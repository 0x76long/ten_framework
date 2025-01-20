#
# Copyright © 2025 Agora
# This file is part of TEN Framework, an open source project.
# Licensed under the Apache License, Version 2.0, with certain conditions.
# Refer to the "LICENSE" file in the root directory for more information.
#
from typing import Optional
from ten import (
    ExtensionTester,
    TenEnvTester,
    Cmd,
    CmdResult,
    TenError,
)


class ExtensionTesterBasic(ExtensionTester):
    def on_register_response(
        self,
        ten_env: TenEnvTester,
        result: Optional[CmdResult],
        error: Optional[TenError],
    ):
        ten_env.log_info("received register response")
        ten_env.stop_test()

    def on_unregister_response(
        self,
        ten_env: TenEnvTester,
        result: Optional[CmdResult],
        error: Optional[TenError],
    ):
        # All ten_env_tester methods will raise exception because on_stop_done()
        # of the extension tester is called.
        exception_caught = False

        try:
            ten_env.log_info("received unregister response")
        except Exception as e:
            print("exception caught: " + str(e))
            exception_caught = True

        assert exception_caught

    def on_start(self, ten_env: TenEnvTester) -> None:
        new_cmd = Cmd.create("register")

        ten_env.log_info("send register cmd")
        ten_env.send_cmd(
            new_cmd,
            lambda ten_env, result, error: self.on_register_response(
                ten_env, result, error  # type: ignore
            ),
        )

        ten_env.on_start_done()

    def on_stop(self, ten_env: TenEnvTester) -> None:
        ten_env.log_info("tester on_stop")

        new_cmd = Cmd.create("unregister")
        ten_env.send_cmd(
            new_cmd,
            lambda ten_env, result, error: self.on_unregister_response(
                ten_env, result, error  # type: ignore
            ),
        )

        ten_env.on_stop_done()


def test_basic():
    tester = ExtensionTesterBasic()
    tester.set_test_mode_single("default_extension_python")
    tester.run()


if __name__ == "__main__":
    test_basic()
