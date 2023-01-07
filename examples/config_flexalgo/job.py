#!/usr/bin/env python

import os

from pyats.easypy import run

SCRIPT = 'test.py'
DATAFILE = 'datafile.yaml'

SCRIPT_DIR = os.path.dirname(__file__)
SCRIPT_PATH = os.path.join(SCRIPT_DIR, SCRIPT)
DATAFILE_PATH = os.path.join(SCRIPT_DIR, DATAFILE)
TASK_ID = os.path.basename(SCRIPT_DIR)

def main(runtime):
    """job file entrypoint"""

    # pyats logs viewでみたときのジョブ名（デフォルトはファイル名から.pyを除いたもの）
    runtime.job.name = TASK_ID

    # run()に渡す引数
    run_args = {
        'runtime': runtime,
        'taskid': TASK_ID,
        'testscript': SCRIPT_PATH
    }

    # データファイルが存在するなら引数に追加
    if os.path.exists(DATAFILE_PATH):
        run_args.update({'datafile': DATAFILE_PATH})

    # pyats.easypy.run()に渡して実行
    run(**run_args)
