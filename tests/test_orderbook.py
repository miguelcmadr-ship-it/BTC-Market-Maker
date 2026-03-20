import time
from orderbook import OrderBook


def test_best_bid_ask_basic():
    ob = OrderBook()

    ob.update_bid(100, 1)
    ob.update_bid(99, 2)

    ob.update_ask(101, 1.5)
    ob.update_ask(102, 3)

    assert ob.best_bid() == (100, 1)
    assert ob.best_ask() == (101, 1.5)


def test_delete_level():
    ob = OrderBook()

    ob.update_bid(100, 1)
    ob.update_bid(100, 0)  # delete

    assert ob.best_bid() is None


def test_mid_price_computation():
    ob = OrderBook()

    ob.update_bid(100, 1)
    ob.update_ask(102, 1)

    mid = ob.mid_price()

    assert mid == 101
    assert ob.data["mid_price"] == 101


def test_mid_price_missing_side():
    ob = OrderBook()

    ob.update_bid(100, 1)

    assert ob.mid_price() is None


def test_volatility_computation():
    ob = OrderBook()

    # simulate mid prices
    ob.prices.extend([100, 101, 102, 101])

    vol = ob.compute_volatility()

    assert vol is not None
    assert vol >= 0


def test_volatility_insufficient_data():
    ob = OrderBook()

    ob.prices.append(100)

    assert ob.compute_volatility() is None


def test_staleness_flag():
    ob = OrderBook()

    ob.update_bid(100, 1)

    # force stale
    ob.last_update_ts = time.time() - 10
    ob.update_staleness(timeout=5)

    assert ob.is_stale is True


def test_not_stale_after_update():
    ob = OrderBook()

    ob.update_bid(100, 1)
    ob.update_staleness(timeout=5)

    assert ob.is_stale is False