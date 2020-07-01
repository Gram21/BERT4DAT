import os
import re
import argparse
from pandas import DataFrame

# filter keywords
keywords = ["public", "private", "final", "static", "const", "override",
            "void", "int", "double", "float", "long", "string",
            "class", "classes", "abstract", "interface", "struct",
            "include", "stdlib", "h", "l"]  # null?


class Config(dict):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for k, v in kwargs.items():
            setattr(self, k, v)

    def set(self, key, val):
        self[key] = val
        setattr(self, key, val)


config = Config(
    class_dir='.',
    out_file='out.tsv',
    max_indent=99999,
    tabsize=2,
    shrink=True,
    no_label=False,
    max_seq_len=512,
    beginning_only=True,
    load_whole=False,
    stop_words=None,
    keywords=keywords,
    split_compound=True,
    filter=True,
    licensefilter=False,
)


def process_camel_case(text):
    return re.sub('([A-Z][a-z]+)', r' \1', re.sub('([A-Z]+)', r' \1', text))


def filter_tokens(tokens):
    if not config.filter:
        return [token.lower() for token in tokens]
    if config.stop_words is None:
        from nltk.corpus import stopwords
        config.stop_words = stopwords.words('english')
    return [token.lower() for token in tokens if token not in (config.stop_words + config.keywords)]


def detokenize(tokens):
    return ' '.join(tokens)


def load_class(classFile):
    lines = []
    inLines = load_file_lines(classFile)

    if config.shrink:
        inLines = shrink_lines(inLines)

    skipMarker = False
    if config.licensefilter:
        skipMarker = True

    # directly filter out certain lines and preprocess/strip lines
    for line in inLines:
        line = line.strip()
        if line.startswith("package"):
            # assumption that license is at the top of the file before the package is declared
            skipMarker = False
        if skipMarker:
            continue
        # strip comment stuff
        line = line.strip(' /*')
        # skip imports and @-Annotations
        if (line.startswith("@") or line.startswith("import")):
            continue
        line = line.strip()
        # remove non alphabetic characters
        line = re.sub("[^a-zA-Z]", " ", line)
        # process camel case if configured to do so
        if config.split_compound:
            line = process_camel_case(line)
        line = line.strip()
        # add line to list of lines if it is not empty
        if line:
            lines.append(line)
    return " ".join(lines)


def process_tokens_of_class_splitting(df, filename, tokens, beginning_only=True):
    label = get_label_from_filename(filename)
    if not label:
        return df
    # split up tokens after max_seq_len and add to dataframe
    for i in range(0, len(tokens), config.max_seq_len):
        start, stop = i, min(i+config.max_seq_len, len(tokens))
        token_slice = tokens[start:stop]
        detokenized_text = detokenize(token_slice)
        if len(detokenized_text) > 1:
            datum = {'file': filename, 'label': label,
                     'text': detokenized_text}
            df = df.append(datum, ignore_index=True)
        if beginning_only:
            break
    return df


def process_tokens_of_class_whole(df, filename, tokens):
    label = get_label_from_filename(filename)
    if not label:
        return df
    detokenized_text = detokenize(tokens)
    if len(detokenized_text) > 1:
        datum = {'file': filename, 'label': label, 'text': detokenized_text}
        df = df.append(datum, ignore_index=True)
    return df


def get_label_from_filename(filename):
    if config.no_label:
        return 'UnknownLabel'
    # Assumption: filename has the form 'LABEL *.*'
    return filename.split()[0].lower()


def load_one_file_into_df(filepath, filename, df):
    text = load_class(filepath)
    tokens = text.split()
    tokens = filter_tokens(tokens)
    if config.load_whole:
        df = process_tokens_of_class_whole(df, filename, tokens)
    else:
        df = process_tokens_of_class_splitting(
            df, filename, tokens, config.beginning_only)
    return df


def load_files_into_df(path, df):
    listing = [os.path.join(dp, f) for dp, dn, fn in os.walk(
        os.path.expanduser(path)) for f in fn]
    listing = list(filter(lambda f: f.endswith('.java'), listing))
    for filepath in listing:
        infile = filepath.replace(path, '', 1).strip('\\/')
        df = load_one_file_into_df(filepath, infile, df)
    return df


def get_sorted_indents(lines):
    return sorted(list(set(indentations(lines))))


def indentation(line):
    expanded_line = line.expandtabs(config.tabsize)
    return 0 if expanded_line.isspace() else len(expanded_line) - len(line.lstrip())


def min_class_indentation(lines):
    min_indent = config.max_indent
    regexp = re.compile(r'\s*class\s+')
    for line in lines:
        if regexp.search(line):
            indent = indentation(line)
            min_indent = indent if indent > 0 and indent < min_indent else min_indent
    return min_indent if min_indent < config.max_indent else 0


def indentations(lines):
    indentations = []
    COMMENT_CHARS = ('*', '//', '/*')
    for line in lines:
        if line.strip().startswith(COMMENT_CHARS):
            continue
        indent = indentation(line)
        indentations.append(indent)
    return indentations


def shrink_lines(lines):
    '''Check the depth of indentation. Indentation one step deeper than class-level is class-body-level; incl. fields and method headers.
    Remove lines with indentation bigger than that (method-body-level) '''
    retLines = []

    class_indent = min_class_indentation(lines)
    indents = get_sorted_indents(lines)
    try:
        class_indent_idx = indents.index(class_indent)
        class_body_indent = indents[class_indent_idx +
                                    1] if len(indents) > class_indent_idx + 1 else class_indent
    except ValueError:
        class_body_indent = class_indent

    for line in lines:
        indent = indentation(line)
        if indent <= class_body_indent + 1 and len(line.strip()) > 0:
            retLines.append(line)

    return retLines


def load_file_lines(filepath):
    '''Load lines of file'''
    with open(filepath, 'r') as file:
        return file.readlines()


def init_argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c", "--classDir", help="Path to the root folder that should be used to recursively look for java-classes")
    parser.add_argument(
        "-o", "--out", help="Path to the file where the output should be saved to")
    parser.add_argument("-l", "--maxSeqLength", type=int, default=512,
                        help="Set the maximum sequence length. Default: 512")
    parser.add_argument("-a", "--all", default=False, action="store_true",
                        help="Set that the classes should not be shrunk (remove method bodies) first.")
    parser.add_argument("-n", "--noLabel", default=False, action="store_true",
                        help="Set whether a label should not be added. Helpful when creating a dataset with unknown labels, e.g., for application")
    parser.add_argument("-r", "--raw", default=False, action="store_true",
                        help="Disable filtering of stopwords.")
    parser.add_argument("-f", "--licensefilter", default=False, action="store_true",
                        help="Enable filtering of license.")
    return parser


if __name__ == "__main__":
    parser = init_argparser()
    args = parser.parse_args()

    config.class_dir = args.classDir
    config.out_file = args.out
    config.max_seq_len = args.maxSeqLength
    config.shrink = not args.all
    config.no_label = args.noLabel
    config.filter = not args.raw
    config.licensefilter = args.licensefilter
    print('Transforming classes in {} and saving the output to {}'.format(
        config.class_dir, config.out_file))

    df = DataFrame(columns=['file', 'label', 'text'])

    print('Loading class-files and processing texts.')
    df = load_files_into_df(config.class_dir, df)
    df = df.dropna()

    print('Finished processing.')

    print("Corpus stats:")
    print(df.shape)
    print(df['label'].value_counts())

    print('Saving texts to ' + config.out_file)
    df.to_csv(config.out_file, sep='\t')
