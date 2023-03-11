import upickle._

@main def dedup(filename: String): Unit = {
  val path = os.pwd / filename
  val json = ujson.read(os.read(path))
  val items = json("items").arr

/* debug only
  val itemsWithMatch = items.filter(
    _("login").obj.get("uris") match {
      case None => false
      case Some(uris) => uris.arr.exists(! _("match").isNull)
    }
  )
  println(itemsWithMatch.length)

  val itemsWithOrganizationId = items.filter(! _("organizationId").isNull)
  println(itemsWithOrganizationId.length)
*/

  // only interested in those fields
  def interested(d: ujson.Value) = {
    val l = d("login").obj
    ( d("organizationId"),
      d("notes"),
      l("username"),
      l("password"),
      l("totp"),
      for {
        uris <- l.get("uris").toList
        uri <- uris.arr
      } yield (uri("match"), uri("uri"))
    )
  }

  val out = items.distinctBy(interested)
  json("items") = out
  val outName = path.baseName + "_out." + path.ext
  
  os.write.over(os.pwd / outName, ujson.write(json))

  println(s"Removed ${items.length - out.length} from ${items.length}, remains ${out.length} entries.")
}
