import warnings

# このファイルがあるディレクトリ名、ここでは'nxos'を抽象化のトークンにする
# これにより os='nxos' を指定してインスタンス化すると、このパッケージに飛んでくる

try:
    from genie import abstract
    abstract.declare_token(__name__)
except Exception as e:
    warnings.warn('Could not declare abstraction token: ' + str(e))
