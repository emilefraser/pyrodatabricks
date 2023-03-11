budget_df = (spark
             .table("products")
             .select("name", "price")
             .where("price < 200")
             .orderBy("price")
            )