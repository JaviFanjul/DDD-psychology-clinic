def test_given_two_registered_queries_when_handling_one_then_it_returns_the_result_of_its_handler(
    query_bus, first_query
):
    result = query_bus.handle(query=first_query)

    assert result == "first result"
