#!/Users/munraito/opt/anaconda3/envs/bdt-python-course/bin/python
import re
import logging
import logging.config
import json
from argparse import ArgumentParser

from lxml import etree
import yaml

APPLICATION_NAME = 'stackoverflow_analytics'
DEFAULT_QUESTION_PATH = 'stackoverflow_posts_sample.xml'
DEFAULT_STOPWORDS_PATH = 'stop_words_en.txt'
DEFAULT_QUERIES_PATH = 'sample_queries.csv'
DEFAULT_LOGGING_CONFIG_PATH = 'logging.conf.yml'

logger = logging.getLogger(APPLICATION_NAME)


class StackOverflowAnalyzer:
    """class for analyzing XMLs from StackOverflow"""

    def __init__(self, stopwords_filepath: str, questions_filepath: str):
        """initialize stopwords and questions dicts"""
        self.stop_words = []
        self.questions = []
        self.parse_stopwords(stopwords_filepath)
        self.parse_questions(questions_filepath)

    def parse_stopwords(self, filepath: str) -> None:
        """method for parsing stopwords file into list"""
        for line in open(filepath, encoding='koi8-r'):
            self.stop_words.append(line[:-1])

    def parse_questions(self, filepath: str) -> None:
        """method for parsing questions file into list excluding stopwords"""
        for line in open(filepath, encoding='utf-8'):
            try:
                xml = etree.fromstring(line)
                if xml.get('PostTypeId') == '1':
                    question = {'year': int(xml.get('CreationDate')[:4]),
                                'score': int(xml.get('Score'))}
                    all_words = set(re.findall(r'\w+', xml.get('Title').lower()))
                    question['words'] = [word for word in all_words if word not in self.stop_words]
                    self.questions.append(question)
            except:  # etree.XMLSyntaxError
                continue

        logger.info('process XML dataset, ready to serve queries')

    def get_words_from_questions(self, start_year: int, end_year: int) -> dict:
        """support method for query"""
        words = {}
        for question in self.questions:
            if start_year <= question['year'] <= end_year:
                for word in question['words']:
                    if word not in words.keys():
                        words[word] = question['score']
                    else:
                        words[word] += question['score']
        return words

    def query(self, filepath: str) -> list:
        """method for querying questions list"""
        answers = []
        for line in open(filepath):
            try:
                start_year, end_year, top_n = list(map(int, line.split(',')))
                logger.debug('got query "%d,%d,%d"', start_year, end_year, top_n)
                words = self.get_words_from_questions(start_year, end_year)
                top_w = sorted(words.items(), key=lambda x: (-x[1], x[0]))[:top_n]
                if len(top_w) < top_n:
                    logger.warning(
                        'not enough data to answer, found %d words out of %d for period "%d,%d"',
                        len(top_w), top_n, start_year, end_year)
                answers.append(json.dumps({'start': start_year, 'end': end_year, 'top': top_w}))
            except:
                continue
        logger.info('finish processing queries')
        return answers


def setup_logging():
    """reads logging configs from YAML"""
    with open(DEFAULT_LOGGING_CONFIG_PATH) as config_file:
        logging.config.dictConfig(yaml.safe_load(config_file))


def setup_parser(parser: ArgumentParser):
    """describes all possible arguments"""
    parser.add_argument("--questions",
                        dest="questions_file", default=DEFAULT_QUESTION_PATH)
    parser.add_argument("--stop-words",
                        dest="stopwords_file", default=DEFAULT_STOPWORDS_PATH)
    parser.add_argument("--queries",
                        dest="queries_file", default=DEFAULT_QUERIES_PATH)


def main():
    """main function"""
    setup_logging()
    parser = ArgumentParser(
        prog='stackoverflow_analytics',
        description="tool to analyze xml from stackoverflow",
    )
    setup_parser(parser)
    args = parser.parse_args()
    analyzer = StackOverflowAnalyzer(args.stopwords_file, args.questions_file)
    for ans in analyzer.query(args.queries_file):
        print(ans)


if __name__ == '__main__':
    main()
