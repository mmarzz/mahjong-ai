import csv
import logging
import os
from optparse import OptionParser

from base.utils.logger import set_up_logging
from base.utils.utils import load_logs
from betaori.parser import BetaoriParser

logger = logging.getLogger('logs')


def main():
    parser = OptionParser()

    parser.add_option(
        '-p', '--protocol',
        type='string',
        help='The output protocol'
    )

    parser.add_option(
        '-o', '--output',
        type='string',
        help='The output file'
    )

    parser.add_option(
        '-d', '--data',
        type='string',
        help='Path to .sqlite3 db with logs content'
    )

    parser.add_option(
        '-l', '--limit',
        type='string',
        help='For debugging',
        default='unlimited'
    )

    opts, _ = parser.parse_args()

    db_path = opts.data
    limit = opts.limit
    output_format = opts.protocol
    output_file = opts.output

    if not db_path:
        parser.error('Path to db is not given.')

    allowed_outputs = {
        'betaori': BetaoriParser()
    }

    if not allowed_outputs.get(output_format):
        parser.error('Not correct output format. Available options: {}'.format(', '.join(allowed_outputs.keys())))

    parser = allowed_outputs.get(output_format)

    if os.path.exists(output_file):
        logger.warning('File {} already exists! New data will append there.'.format(output_file))
    else:
        with open(output_file, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(parser.csv_exporter.header())

    set_up_logging('parser')

    logger.info('Loading and decompressing logs content...')
    logs = load_logs(db_path, limit)

    logs_count = 0
    samples_count = 0
    count_of_logs = len(logs)
    logger.info('Starting processing {} logs...'.format(count_of_logs))

    for log_data in logs:
        if logs_count > 0 and logs_count % 1000 == 0:
            logger.info('Processed logs: {}/{}'.format(logs_count, count_of_logs))
            logger.info('Samples: {}'.format(samples_count))

        game = parser.get_game_rounds(log_data['log_content'], log_data['log_id'])
        records = parser.parse_game_rounds(game)
        samples_count += len(records)

        with open(output_file, 'a') as f:
            writer = csv.writer(f)
            for record in records:
                writer.writerow(record)

    logger.info('End')
    logger.info('Total samples:  {}'.format(samples_count))


if __name__ == '__main__':
    main()