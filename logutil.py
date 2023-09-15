import logging
import logging.config

# Simpler method that sets the level everywhere, then makes exclusions for specific loggers/libraries

logging.basicConfig(
    # filename = 'src/log.txt',
    format = "%(levelname) -10s %(asctime)s %(filename)s:%(lineno)s %(name)s.%(funcName)s | %(message)s",
    level=logging.DEBUG
)

level_override = {
    logging.INFO: {
        'internal': [],
        'external': [],
    },
    logging.WARNING: {
        'internal': [],
        'external': ['matplotlib', 'matplotlib.pyplot', 'PIL.PngImagePlugin', 
                     'selenium', 'connectionpool', 'urllib3'],
    }
}

for level, level_loggers in level_override.items():
    for logger in level_loggers['internal'] + level_loggers['external']:
        logging.getLogger(logger).setLevel(level)