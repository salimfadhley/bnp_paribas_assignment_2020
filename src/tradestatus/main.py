import logging

import click

from tradestatus.model import run_trade_summary


@click.command()
@click.option(
    "-o", "--output_path", default="results.csv", help="Path of the output file."
)
@click.option(
    "-l",
    "--log_file",
    default="server.log",
    help="Log file for errors and information.",
)
@click.argument("input_path")
def main(input_path: str, output_path: str, log_file: str):
    logging.basicConfig()
    root_logger = logging.getLogger(__name__)
    root_logger.setLevel(logging.INFO)

    fhf = logging.Formatter(fmt="'%(asctime)s - %(levelname)s - %(message)s'")

    fh = logging.FileHandler(log_file)
    log.info(f"Writing logs to {log_file}")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(fhf)

    root_logger.addHandler(fh)
    log.info("Trade status command beginning.")
    log.info(f"Writing output to {output_path}")

    try:
        with open(input_path) as input_stream, open(output_path, "w") as output_stream:
            run_trade_summary(input_stream, output_stream)
    except RuntimeError as rte:
        log.exception("Abnormal termination.")
    finally:
        log.info("Trade status command finished.")


log = logging.getLogger(__name__)
