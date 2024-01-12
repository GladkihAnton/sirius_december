from app.core.config import Config

API_PREFIX = "/sirius" + Config.API_V1_STR

URLS = {
    "sirius":{
        "api": {
            "v1": {
                "token":{
                    "login": API_PREFIX + "/token/login",
                    "info": API_PREFIX + "/token/info",
                },
                "user": {

                    "create": API_PREFIX + "/user/create",
                    "get": API_PREFIX + "/user/get",
                },
                "cart":{
                    "add_to_cart": API_PREFIX + "/cart/add_to_cart",
                    "place_order": API_PREFIX + "/cart/place_order",
                    "update_cart_product": API_PREFIX + "/cart/update_cart_product/",
                    "remove_from_cart": API_PREFIX + "/cart/remove_from_cart/",
                    "get_cart": API_PREFIX + "/cart/get_cart/{order_id}",
                },
                "product":{
                    "create_product": API_PREFIX + "/product/create_product",
                    "update_product": API_PREFIX + "/product/update_product/",
                    "delete_product": API_PREFIX + "/product/delete_product/",
                    "get_all_products": API_PREFIX + "/product/get_all_products",
                }
            }
        }
    }
    
}