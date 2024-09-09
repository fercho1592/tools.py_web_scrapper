'''File to get the settings'''
import configparser

def read_config():
  # Create a ConfigParser object
  config = configparser.ConfigParser()

  # Read the configuration file
  config.read('config.ini')

  # Access values from the configuration file
  log_level = config.get('General', 'log_level')
  e_manga_strategy = config.get('MangaStrategy', 'e_manga_domain')

  # Return a dictionary with the retrieved values
  config_values = {
    'log_level': log_level,
    'e_manga_domain': e_manga_strategy,
  }

  return config_values
