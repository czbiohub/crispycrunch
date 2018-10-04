import doctest
import re

from django.core.exceptions import ValidationError

# See also CHR_REGEX in conversions.py
CHR_REGEX = r'^chr([0-9XY]+):([0-9,]+)-([0-9,]+[0-9])$'
# See https://www.genenames.org/about/guidelines
# And see https://www.biostars.org/p/60118/ .
GENE_REGEX = r'^[A-Z0-9-]+$|^C[0-9XY]+orf[0-9]+$'


def validate_fastq(filename: str) -> None:
    """
    >>> validate_fastq('crispresso/fastqs/A1-ATL2-N-sorted-180212_S1_L001_R1_001.fastq')
    >>> validate_fastq('crispresso/fastqs/A1-ATL2-N-sorted-180212_S1_L001_R1_001.fastq.gz')
    >>> validate_fastq('crispresso/fastqs/A1-ATL2-N-sorted-180212_S1_L001_R1_001.fa')
    Traceback (most recent call last):
    ...
    django.core.exceptions.ValidationError: ['"crispresso/fastqs/A1-ATL2-N-sorted-180212_S1_L001_R1_001.fa" is not a valid fastq file']
    """
    if (not filename.endswith('.fastq') and not filename.endswith('.fastq.gz')):
        raise ValidationError('"{}" is not a valid fastq file'.format(filename))


def validate_seq(value: str) -> None:
    """
    See https://en.wikipedia.org/wiki/Nucleic_acid_sequence.

    Also allows a trailing space separated PAM.

    >>> validate_seq('gtca')
    >>> validate_seq('CACTGCAACCTTGGCCTCCC GGG')
    >>> validate_seq('asdf')
    Traceback (most recent call last):
    ...
    django.core.exceptions.ValidationError: ['"asdf" is not a nucleic acid sequence']
    """
    if re.match(r'^[ACGTRYKMSWBDHVN]+( [ACGTRYKMSWBDHVN]{3})?$', value.upper()) is None:
        raise ValidationError('"{}" is not a nucleic acid sequence'.format(value))


def is_seq(value: str) -> bool:
    """
    >>> is_seq('gtca')
    True
    >>> is_seq('asdf')
    False
    """
    try:
        validate_seq(value)
    except ValidationError:
        return False
    else:
        return True


def validate_chr(value: str) -> None:
    """
    >>> validate_chr('chr1:11,130,540-11,130,751')

    >>> validate_chr('chrX:153701031-153701090')

    >>> validate_chr('chr1:11,130,540-11,130,751,')
    Traceback (most recent call last):
    ...
    django.core.exceptions.ValidationError: ['"chr1:11,130,540-11,130,751," is not a chromosome location']

    >>> validate_chr('chrA:11,130,540-11,130,751')
    Traceback (most recent call last):
    ...
    django.core.exceptions.ValidationError: ['"chrA:11,130,540-11,130,751" is not a chromosome location']
    """
    if re.match(CHR_REGEX, value) is None:
        raise ValidationError('"{}" is not a chromosome location'.format(value))


def validate_chr_length(value: str, max_length: int = 2000) -> None:
    """
    >>> validate_chr_length('chr1:11,130,540-11,130,751')
    >>> validate_chr_length('chr1:11,230,540-11,130,751')
    Traceback (most recent call last):
    ...
    django.core.exceptions.ValidationError: ['"99789" is longer than the max length of 2000']
    """
    matches = [m.replace(',', '') for m in re.match(CHR_REGEX, value).groups()]  # type: ignore
    length = abs(int(matches[1]) - sum(int(m) for m in matches[2:]))
    if length > max_length:
        raise ValidationError('"{}" is longer than the max length of {}'.format(
            length, max_length))


def is_chr(value: str) -> bool:
    """
    >>> is_chr('chr1:11,130,540-11,130,751')
    True
    >>> is_chr('gtca')
    False
    """
    try:
        validate_chr(value)
    except ValidationError:
        return False
    return True


def validate_ensemble_transcript(value: str) -> None:
    """
    >>> validate_ensemble_transcript('EENST00000330949')
    Traceback (most recent call last):
    ...
    django.core.exceptions.ValidationError: ['"EENST00000330949" is not a Ensembl transcript ID']
    """
    if re.match(r'^ENST[0-9]+$', value) is None:
        raise ValidationError('"{}" is not a Ensembl transcript ID'.format(value))


def is_ensemble_transcript(value: str) -> bool:
    """
    >>> is_ensemble_transcript('ENST00000330949')
    True
    >>> is_ensemble_transcript('ENST00000398844')
    True
    >>> is_ensemble_transcript('EENST00000330949')
    False
    """
    try:
        validate_ensemble_transcript(value)
    except ValidationError:
        return False
    else:
        return True


def validate_chr_or_seq_or_enst_or_gene(value: str) -> None:
    if not any((
            is_chr(value),
            is_seq(value),
            is_ensemble_transcript(value),
            is_gene(value))):
        raise ValidationError(
            '"{}" is not a chromosome location or nucleic acid sequence or a Ensembl transcript ID or a HGNC gene name'.format(value))
    if is_chr(value):
        validate_chr_length(value)
        # TODO (gdingle): length of other types


def get_guide_loc(target_loc: str, guide_offset: int, guide_len=20) -> str:
    """
    # TODO (gdingle): is this actually correct def for guide_loc?
    >>> get_guide_loc('chr7:5569177-5569415', 191)
    'chr7:5569348-5569367'
    """
    validate_chr(target_loc)
    matches = re.match(CHR_REGEX, target_loc).groups()  # type: ignore
    start = int(matches[1]) + guide_offset
    # TODO (gdingle): is this correct for reverse guides?
    # Guide goes backwards from pam, right to left
    # Minus one, for length inclusive
    return 'chr{}:{}-{}'.format(matches[0], start - guide_len, start - 1)


def get_guide_cut_to_insert(target_loc: str, guide_loc: str) -> int:
    """
    Based on https://czi.quip.com/YbAhAbOV4aXi/

    >>> get_guide_cut_to_insert('chr5:134649077-134649174', 'chr5:134649061-134649080')
    -2
    >>> get_guide_cut_to_insert('chr5:134649077-134649174', 'chr5:134649077-134649096')
    14
    """
    validate_chr(target_loc)
    validate_chr(guide_loc)
    target_matches = re.match(CHR_REGEX, target_loc).groups()  # type: ignore
    # insert location is assumed to be always one codon past start codon
    insert_loc = int(target_matches[1]) + 3

    guide_matches = re.match(CHR_REGEX, guide_loc).groups()  # type: ignore
    # cut location is assumed to be always in between the 3rd and 4th nucleotide
    # away from the PAM site
    cut_loc = int(guide_matches[2]) - 3
    # TODO (gdingle): is this correct for reverse guides?
    # Plus one for inclusive range
    return cut_loc - insert_loc + 1


def get_hdr_template(target_seq: str, hdr_seq: str) -> str:
    """
    Based on https://czi.quip.com/YbAhAbOV4aXi/

    >>> get_hdr_template('ATGTCCCAGCCGGGAAT', 'NNN')
    'ATGNNNTCCCAGCCGGGAAT'
    """
    validate_seq(target_seq)
    validate_seq(hdr_seq)
    return target_seq[0:3] + hdr_seq + target_seq[3:]


def get_primer_loc(primer_product: str, guide_seq: str, guide_loc: str) -> str:
    """
    Returns the chr loc of a primer product seq based on the known position of
    the guide within it.

    >>> get_primer_loc('''TGCTGGCTGGCCATTTCTAAACTTCCATTTGAATTTAANNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN
    ... NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN
    ... NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN
    ... NNNNNNNNNNNNNNNNNNNNNNNTATTACTTTTGTCTTCTACTAGCCAAAAGAATGTCAACAGAAATCAGAACATAACAC
    ... TAAGTAAGTTTAACATGTACTTTTATTAACAACTTAATACAAGACTGTACACTGTAGGTGCTGAAATCAACCCACTCCT''',
    ... 'AATACAAGACTGTACACTGTAGG', 'chr2:136114380-136114402')
    'chr2:136114025-136114423'
    """
    primer_product = primer_product.replace('\n', '')
    # TODO (gdingle): time to start using seq objects? Biopython?
    validate_seq(primer_product)
    validate_seq(guide_seq)
    validate_chr(guide_loc)
    assert guide_seq in primer_product
    chr_num, start, end = re.match(CHR_REGEX, guide_loc).groups()  # type: ignore
    start, end = int(start), int(end)
    assert end - start == len(guide_seq) - 1  # inclusive range

    primer_start = start - primer_product.index(guide_seq)
    primer_end = primer_start + len(primer_product) - 1
    assert primer_end - primer_start <= 500, 'Primers should always be less than 500 bp for paired reads'
    assert primer_end - primer_start == len(primer_product) - 1

    return 'chr{}:{}-{}'.format(chr_num, primer_start, primer_end)


def validate_gene(value: str) -> None:
    """
    >>> validate_gene('ATL2') is None
    True
    >>> validate_gene('atl2')
    Traceback (most recent call last):
    ...
    django.core.exceptions.ValidationError: ['"atl2" is not a valid HGNC gene name']
    """
    if re.match(GENE_REGEX, value) is None:
        raise ValidationError('"{}" is not a valid HGNC gene name'.format(value))


def is_gene(value: str) -> bool:
    """
    >>> is_gene('ATL3')
    True
    >>> is_gene('ATL_3')
    False
    """
    try:
        validate_gene(value)
    except ValidationError:
        return False
    else:
        return True


def validate_num_wells(value: dict, max: int = 96) -> None:
    total = sum(len(seqs) for seqs in value.values())
    if total > max:
        raise ValidationError(
            '{} items do not fit in a 96-well plate'.format(total))


if __name__ == '__main__':
    doctest.testmod()
