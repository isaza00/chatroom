from django.test import TestCase
from .tasks import get_bot_message



class BotTestCase(TestCase):

    def test_get_bot_message(self):
        """Should return bot meesage from pattern /stock=aapl"""

        message = "/stock=aapl"
        bot_message = get_bot_message(message)

        self.assertIn('AAPL.US quote is $', bot_message)
        self.assertIn('per share', bot_message)

    def test_get_bot_error_message_on_empty_string(self):
        """Should return error bot message from pattern /stock="""

        message = "/stock="
        bot_message = get_bot_message(message)
        
        self.assertIn('There is no data for requested symbol', bot_message)

    def test_get_bot_error_message_on_wrong_string(self):
        """Should return error bot message from pattern /stock=wrong"""

        message = "/stock=wrong"
        bot_message = get_bot_message(message)
        
        self.assertIn('There is no data for requested symbol', bot_message)
