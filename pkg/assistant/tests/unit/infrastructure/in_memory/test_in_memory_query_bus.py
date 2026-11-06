async def test_given_two_registered_queries_when_handling_one_then_it_returns_its_handler_result(
    query_bus, first_query
):
    result = await query_bus.handle(query=first_query)

    assert result == "first result"
