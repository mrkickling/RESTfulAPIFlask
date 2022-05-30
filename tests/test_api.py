import os, sys, inspect, time
import unittest
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from app.apihandler import ApiHandler
from app.utils import random_string
from app.message import Message

ONE_DAY_SECONDS = 24 * 60 * 60

class TestApiHandler(unittest.TestCase):
    def test_write_message(self):
        handler = ApiHandler()
        res = handler.write_message("text", "hostname")
        assert res["success"] == 1
        assert len(handler.messages) == 1
        assert len(handler.time_sorted_message_ids) == 1
        
        res = handler.write_message("text2", "hostname")
        assert res["success"] == 1
        assert len(handler.messages) == 2
        assert len(handler.time_sorted_message_ids) == 2

    def test_write_long_message(self):
        handler = ApiHandler()
        very_long_string = random_string(1024 * 1024)
        res = handler.write_message(very_long_string, "hostname")
        assert res["success"] == 0, "message was too long"
        assert len(handler.messages) == 0, "should not be added to list"
        assert len(handler.time_sorted_message_ids) == 0, "should not be added to list"
 
    def test_read_message(self):
        handler = ApiHandler()
        string_to_write = random_string(1000)
        res = handler.write_message(string_to_write, "hostname")

        true_id = res["message_id"]
        random_id = random_string(12)

        # Read a random ID, should fail
        res = handler.read_message(random_id)
        assert res["success"] == 0, "Should not succeed"
        
        # Read the true ID, should work
        res = handler.read_message(true_id)
        assert res["success"] == 1, "Should definitely succeed"

    def test_delete_old_messages(self):
        handler = ApiHandler()
        message_id = random_string(12)
        message = Message(message_id, "text", "hostname", time.time() - 7 * ONE_DAY_SECONDS)
        handler.save_message(message)
        assert len(handler.messages) == 1
        assert len(handler.time_sorted_message_ids) == 1
        time.sleep(15)
        res = handler.read_message(message_id)
        assert res["success"] == 0, "Should not be able to get old message"
        assert len(handler.messages) == 0, "Old message should be removed from list"
        assert len(handler.time_sorted_message_ids) == 0, "Old message should be removed from list"

    def test_six_day_old_messages(self):
        handler = ApiHandler()
        message_id = random_string(12)
        message = Message(message_id, "text", "hostname", time.time() - 6 * ONE_DAY_SECONDS)
        handler.save_message(message)
        time.sleep(15)
        # Should be able to read 6 day old message
        res = handler.read_message(message_id)
        assert res["success"] == 1, "Should be able to get old message"
        assert len(handler.messages) == 1, "Old message should be in list"
        assert len(handler.time_sorted_message_ids) == 1, "Old message should be in list"


if __name__ == "__main__":
    unittest.main()