def test_given_two_handlers_of_an_event_when_publishing_it_then_only_they_receive_it(
    event_bus,
    first_handler_of_first_event,
    second_handler_of_first_event,
    handler_of_second_event,
    first_event,
):
    event_bus.publish(events=[first_event])

    assert first_handler_of_first_event.handled == [first_event]
    assert second_handler_of_first_event.handled == [first_event]
    assert handler_of_second_event.handled == []


def test_given_two_events_when_publishing_both_then_each_handler_receives_its_own(
    event_bus, first_handler_of_first_event, handler_of_second_event, first_event, second_event
):
    event_bus.publish(events=[first_event, second_event])

    assert first_handler_of_first_event.handled == [first_event]
    assert handler_of_second_event.handled == [second_event]


def test_given_an_event_without_handlers_when_publishing_it_then_nothing_fails(
    event_bus, first_handler_of_first_event, handler_of_second_event, unhandled_event
):
    event_bus.publish(events=[unhandled_event])

    assert first_handler_of_first_event.handled == []
    assert handler_of_second_event.handled == []
