const post_to_get_urls = ["login"]
module.exports = function (req, res, next) {
  // convert requests to GET, if in whitelist
  for (let url of post_to_get_urls) {
    if (req.originalUrl.includes(url) && ["POST", "PUT"].indexOf(req.method) !== -1) {
      req.method = "GET"
      req.query = req.body
    }
  }
  // Continue to JSON Server router
  next()
}
