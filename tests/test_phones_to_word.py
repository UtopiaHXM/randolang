from unittest import TestCase

from phones_to_word import phones_to_word
from word_data import entries_from_cmudict, filter_entries
from randolang import _clean_phones


class TestPhonesToWord(TestCase):
    def test_phones_to_word(self):
        cases = [
            (['B', 'IH', 'D'], ['bid']),
            (['C', 'R', 'IY', 'EY', 'T'], ['create', 'creeate']),
            (
                ['AH', 'N', 'G', 'R', 'EY', 'T', 'F', 'AH', 'L'],
                ['ungrateful', 'ungraitful']
            )
        ]
        for case in cases:
            phones, spellings = case
            calculated_word = phones_to_word(phones)
            self.assertIn(calculated_word, spellings)

    def test_words_correct(self):
        """Test the accuracy of the spelling against existing words."""
        entries = entries_from_cmudict()
        entries = filter_entries(entries, 'Austen')
        number_correct = 0
        for entry in entries:
            word, phones = entry
            # clean_phone modifies phones in-place, so
            cleaned_phones = _clean_phones(phones)
            calculated_word = phones_to_word(cleaned_phones)
            if word == calculated_word:
                number_correct += 1
            else:
                print "Incorrect spelling. Expected %s, got %s. Phones: %s" % (
                    word, calculated_word, phones
                )
        self.assertEqual(number_correct, 1001)
