import os
import time
from concurrent.futures import ThreadPoolExecutor
import argparse
import logging


def log_time(level=logging.INFO):
    def decorator(func):
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            end = time.perf_counter()
            elapsed = end - start
            log.log(level, f"Function '{func.__name__}' executed in {elapsed:.4f} seconds")
            return result

        return wrapper

    return decorator


@log_time()
def load_xml(path):
    with open(path, "rb") as f:
        tree = etree.parse(f)
    return tree


@log_time(logging.DEBUG)
def check_xpath(tree, xpath_expr, **kwargs):
    repeat = kwargs.get("repeat", 1)
    results = []
    for i in range(repeat):
        results = tree.xpath(xpath_expr)
    log.debug(f"{xpath_expr} found: {len(results)}")


@log_time(logging.DEBUG)
def check_findall(tree, xpath_expr, **kwargs):
    repeat = kwargs.get("repeat", 1)
    results = []
    for i in range(repeat):
        results = tree.findall(xpath_expr)
    log.debug(f"{xpath_expr} found: {len(results)}")


@log_time(logging.DEBUG)
def root_iter(tree, xpath_exp, **kwargs):
    repeat = kwargs.get("repeat", 1)
    for i in range(repeat):
        for elem in tree.iter():
            continue


def check_runner(max_threads, test_method, tree, all_xpaths, **kwargs):
    start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = [executor.submit(test_method, tree, xp, **kwargs) for xp in all_xpaths]
        for f in futures:
            f.result()
    end = time.perf_counter()
    elapsed = end - start
    log.info(f"Function '{kwargs.get('name')}' executed in {elapsed:.4f} seconds")


@log_time()
def main(max_threads=None, repeat=1):
    tree = load_xml(XML_FILE)
    tags = {elem.tag for elem in tree.iter()}
    all_xpaths = [f"//{tag}" for tag in tags]
    if max_threads is None:
        max_threads = len(all_xpaths)
    while max_threads > len(all_xpaths):
        log.debug("More threads than jobs. Adding more xpaths")
        all_xpaths.append(all_xpaths[0])

    check_runner(max_threads, check_xpath, tree, all_xpaths, repeat=repeat, name="check_xpath")
    check_runner(max_threads, check_findall, tree, all_xpaths, repeat=repeat, name="find_all")
    check_runner(max_threads, root_iter, tree, all_xpaths, repeat=repeat, name="root_iter")


if __name__ == "__main__":
    import sys

    py_v_major = sys.version_info.major
    py_v_minor = sys.version_info.minor
    try:
        gil_enabled = sys._is_gil_enabled()
    except AttributeError:
        gil_enabled = True
    parser = argparse.ArgumentParser()
    parser.add_argument("--repeat",
                        type=int,
                        default=1,
                        help="repeat each check given number")
    parser.add_argument("--max-threads",
                        type=int,
                        default=8,
                        help="run checks in threads")
    parser.add_argument("--use-preinstalled-lxml",
                        action="store_true",
                        default=False,
                        help="use lxml that was installed using pip, not built from source")
    parser.add_argument("--log-level",
                        type=int,
                        default=logging.INFO,
                        help="set log level")
    args = parser.parse_args()

    if not args.use_preinstalled_lxml:
        try:
            sys.path.insert(0, f"lxml/build/lib.linux-x86_64-cpython-{py_v_major}{py_v_minor}")
            import lxml
            from lxml import etree
        except ImportError:
            if not gil_enabled:
                sys.path.pop(0)
                sys.modules.pop("lxml", None)
                sys.path.insert(0, f"lxml/build/lib.linux-x86_64-cpython-{py_v_major}{py_v_minor}t")
                import lxml
                from lxml import etree
    else:
        import lxml
        from lxml import etree

    log_level = args.log_level
    os.makedirs("logs", exist_ok=True)
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        filename=f"logs/test_lxml_{py_v_major}{py_v_minor}{'' if gil_enabled else 't'}_{lxml.__version__}.log",
        filemode="a",
    )
    stream_logger = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    stream_logger.setFormatter(formatter)
    stream_logger.setLevel(log_level)

    log = logging.getLogger()
    log.addHandler(stream_logger)

    # Path to your XML file
    XML_FILE = "example.xml"
    log.info("Start script")
    log.info(f"Python: {py_v_major}.{py_v_minor}, "
             f"free threaded: {not gil_enabled}, "
             f"lxml version: {lxml.__version__}")
    log.info(args)

    main(max_threads=args.max_threads, repeat=args.repeat)
