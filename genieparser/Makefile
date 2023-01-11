PYTHON = python

# usage: folder_parsing_job.py [-h] [-o OPERATING_SYSTEM] [-c CLASS_NAME] [-t TOKEN] [-f] [-n NUMBER] [-e EXTERNAL_FOLDER] [--show-missing-unittests]
#
# Optional arguments for 'nose'-like tests
#
# optional arguments:
#   -h, --help            show this help message and exit
#   -o OPERATING_SYSTEM, --operating_system OPERATING_SYSTEM
#                         The OS you wish to filter on
#   -c CLASS_NAME, --class_name CLASS_NAME
#                         The Class you wish to filter on, (not the Test File)
#   -t TOKEN, --token TOKEN
#                         The Token associated with the class, such as 'asr1k'
#   -f, --display_only_failed
#                         Displaying only failed classes
#   -n NUMBER, --number NUMBER
#                         The specific unittest we want to run, such as '25'
#   -e EXTERNAL_FOLDER, --external-folder EXTERNAL_FOLDER
#                         An external parser folder to work with
#   --show-missing-unittests
#                         Print out parsers that are missing unittests

# cd tests
# python folder_parsing_job.py -e ../external_parser -o fitelnet -c Dir
# python folder_parsing_job.py -e ../external_parser -o fitelnet -c Ping
# python folder_parsing_job.py -e ../external_parser -o fitelnet -c ShowBoot
# python folder_parsing_job.py -e ../external_parser -o fitelnet -c ShowInterface
# python folder_parsing_job.py -e ../external_parser -o fitelnet -c ShowIpBgpNeighbors
# python folder_parsing_job.py -e ../external_parser -o fitelnet -c ShowIpBgpVpnv4AllDetail
# python folder_parsing_job.py -e ../external_parser -o fitelnet -c ShowIpInterfaceBrief
# python folder_parsing_job.py -e ../external_parser -o fitelnet -c ShowIsisFlexAlgo
# python folder_parsing_job.py -e ../external_parser -o fitelnet -c ShowIsisInterfaceDetail
# python folder_parsing_job.py -e ../external_parser -o fitelnet -c ShowIsisNeighborDetail
# python folder_parsing_job.py -e ../external_parser -o fitelnet -c ShowIsisNeighbor
# python folder_parsing_job.py -e ../external_parser -o fitelnet -c ShowSegmentRoutingSrv6Locator
# python folder_parsing_job.py -e ../external_parser -o fitelnet -c ShowSegmentRoutingSrv6Sid
# python folder_parsing_job.py -e ../external_parser -o fitelnet -c ShowSegmentRoutingSrv6SidCounter
# python folder_parsing_job.py -e ../external_parser -o fitelnet -c ShowSegmentRoutingSrv6SidDetail
# python folder_parsing_job.py -e ../external_parser -o fitelnet -c ShowVersion

test:
	@(cd tests; python folder_parsing_job.py -e ../external_parser -o fitelnet)
