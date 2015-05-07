#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/atmospheres/")

from atmospheres.controller import web_service as application
