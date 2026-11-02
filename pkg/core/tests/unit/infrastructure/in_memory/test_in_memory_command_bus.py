async def test_given_two_registered_commands_when_handling_one_then_only_its_handler_receives_it(
    command_bus, first_handler, second_handler, first_command
):
    await command_bus.handle(command=first_command)

    assert first_handler.handled == [first_command]
    assert second_handler.handled == []
