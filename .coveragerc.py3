[run]
source = cirrocumulus


[report]
omit =
    */python?.?/*
    */lib-python/?.?/*
    */lib_pypy/*
    */site-packages/nose/*

exclude_lines =
    pragma: no cover
    pragma: no cover [py3]
    def __repr__
    raise NotImplementedError
    assert False,
    if 0:
    if __name__ == .__main__.:


; vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8:
