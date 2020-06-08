from server import utils
from server import cache
import requests
import config

class General():
    @classmethod
    def info(cls):
        data = utils.make_request("getblockchaininfo")

        if data["error"] is None:
            data["result"]["supply"] = utils.supply(data["result"]["blocks"])["supply"]
            data["result"]["reward"] = utils.reward(data["result"]["blocks"])

            nethash = utils.make_request("getnetworkhashps", [6, data["result"]["blocks"]])
            if nethash["error"] is None:
                data["result"]["nethash"] = int(nethash["result"])

        return data

    @classmethod
    @cache.memoize(timeout=config.cache)
    def supply(cls):
        data = utils.make_request("getblockchaininfo")
        height = data["result"]["blocks"]
        result = utils.supply(height)
        result["height"] = height

        return result

    @classmethod
    def fee(cls):
        # ToDo: Fix me
        # https://github.com/sugarchain-project/sugarchain/issues/34

        # data = utils.make_request("estimatesmartfee", [6])

        # if data["error"] is None:
        #   data["result"]["feerate"] = utils.satoshis(data["result"]["feerate"])

        # return data

        return utils.response({
            "feerate": utils.satoshis(0.00001),
            "blocks": 6
        })

    @classmethod
    def mempool(cls):
        data = utils.make_request("getmempoolinfo")

        if data["error"] is None:
            if data["result"]["size"] > 0:
                mempool = utils.make_request("getrawmempool")["result"]
                data["result"]["tx"] = mempool
            else:
                data["result"]["tx"] = []

        return data

    @classmethod
    def price(cls):
        link = "https://api.coingecko.com/api/v3/simple/price?ids=sugarchain&vs_currencies=usd,btc"
        return requests.get(link).json()
