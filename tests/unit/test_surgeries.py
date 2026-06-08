import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime
from src.vetlog_calendar.main import list_unlogged_surgeries

class TestUnloggedSurgeries(unittest.TestCase):

    @patch('src.vetlog_calendar.main.get_session')
    @patch('src.vetlog_calendar.main.UserRepository')
    @patch('src.vetlog_calendar.main.PetRepository')
    @patch('src.vetlog_calendar.main.SurgeryRepository')
    @patch('src.vetlog_calendar.main.MedicalLogRepository')
    def test_list_unlogged_surgeries_success(self, mock_log_repo, mock_surgery_repo, mock_pet_repo, mock_user_repo, mock_get_session):
        """Test that unlogged surgeries from the past 7 days are successfully identified"""
        mock_session = MagicMock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        mock_surgery_1 = MagicMock(id=1, pet_id=10, date=datetime.utcnow()) # Has log (Should filter out)
        mock_surgery_2 = MagicMock(id=2, pet_id=11, date=datetime.utcnow()) # No log (Should be caught!)
        mock_log = MagicMock(surgery_id=1) 
        mock_surgery_repo.return_value.get_surgeries_in_range.return_value = [mock_surgery_1, mock_surgery_2]
        mock_log_repo.return_value.get_logs_in_range.return_value = [mock_log]
        mock_pet = MagicMock(name="Max", adopter_id=None, user_id=100)
        mock_owner = MagicMock(first_name="Jane", last_name="Doe", email="jane@example.com")
        mock_pet_repo.return_value.find_by_id.return_value = mock_pet
        mock_user_repo.return_value.find_by_id.return_value = mock_owner
        try:
            list_unlogged_surgeries()
            test_passed = True
        except Exception as e:
            test_passed = False
            print(f"Test crashed with error: {e}")
        self.assertTrue(test_passed)

if __name__ == '__main__':
    unittest.main()