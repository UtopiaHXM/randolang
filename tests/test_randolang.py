from unittest import TestCase

from randolang import (
    generate_transitions, _clean_phones,
    generate_transitions_dict, add_transition_to_dict,
    order_from_transitions_dict, generate_word, _generate_phone,
    entries_from_cmudict, austen_words)





class TestGenerateTransitions(TestCase):
    def test_first_order_transitions(self):
        phones = ['K0', 'UH1', 'T0']
        transitions = generate_transitions(phones)
        self.assertEqual(
            transitions,
            [
                ['START', 'K'],
                ['K', 'UH'],
                ['UH', 'T'],
                ['T', 'STOP']
            ]
        )
    def test_second_order_transitions(self):
        phones = ['K', 'UH', 'T']
        transitions = generate_transitions(phones, order=2)
        self.assertEqual(
            transitions,
            [
                ['START', 'START', 'K'],
                ['START', 'K', 'UH'],
                ['K', 'UH', 'T'],
                ['UH', 'T', 'STOP'],
                ['T', 'STOP', 'STOP']
            ]
        )

class TestCleanPhones(TestCase):
    def test_clean_phones(self):
        phones = ['AA1']
        cleaned_phones = _clean_phones(phones)
        self.assertEqual(cleaned_phones, ['AA'])

class TestGenerateTransitionsDict(TestCase):
    def setUp(self):
        self.entries = [
            ('booboo', ['B0', 'UW1', 'B', 'UW1'])
        ]

    def test_generate_transitions_dict(self):
        transitions_dict = generate_transitions_dict(self.entries, order=1)
        self.assertEqual(
            transitions_dict,
            {
                'START': {
                    'B': 1
                },
                'B': {
                    'UW': 2
                },
                'UW': {
                    'B': 1,
                    'STOP': 1
                }
            }
        )

    def test_second_order(self):
        transitions_dict = generate_transitions_dict(self.entries, order=2)
        self.assertEqual(
            transitions_dict,
            {
                'START': {
                    'START': {
                        'B': 1
                    },
                    'B': {
                        'UW': 1,
                    }
                },
                'B': {
                    'UW': {
                        'B': 1,
                        'STOP': 1
                    }
                },
                'UW': {
                    'B': {
                        'UW': 1
                    },
                    'STOP': {
                        'STOP': 1
                    }
                }
            }
        )

class AddTransitionTestCase(TestCase):
    def test_add_first_order(self):
        transition = ('B', 'UW')
        transitions_dict = {
            'B': {
                'AH': 1
            }
        }
        add_transition_to_dict(transitions_dict, transition)
        self.assertEqual(
            transitions_dict,
            {
                'B': {
                    'AH': 1,
                    'UW': 1
                }
            }
        )

    def test_add_second_order(self):
        transition = ('B', 'UW', 'K')
        transitions_dict = {
            'B': {
                'AH': {
                    'T': 1
                }
            }
        }
        add_transition_to_dict(transitions_dict, transition)
        self.assertEqual(
            transitions_dict,
            {
                'B': {
                    'AH': {
                        'T': 1
                    },
                    'UW': {
                        'K': 1
                    }
                }
            }
        )

class OrderFromTransitionsDictTest(TestCase):
    def test_first_order_transitions_dict(self):
        transitions_dict = {
            'B': {
                'AH': 1
            }
        }
        order = order_from_transitions_dict(transitions_dict)
        self.assertEqual(order, 1)

    def test_second_order_transitions_dict(self):
        transitions_dict = {
            'B': {
                'UH': {
                    'B': 1
                }
            }
        }
        order = order_from_transitions_dict(transitions_dict)
        self.assertEqual(order, 2)

class GenerateWordTest(TestCase):
    def test_first_order_word(self):
        transitions_dict = {
            'START': {
                'B': 1
            },
            'B': {
                'UH': 1
            },
            'UH': {
                'STOP': 1
            }
        }
        word = generate_word(transitions_dict, 10)
        self.assertEqual(word, 'buh')

    def test_long_word_cutoff(self):
        transitions_dict = {
            'START': {
                'B': 1
            },
            'B': {
                'UH': 1
            },
            'UH': {
                'L': 1
            },
            'L': {
                'STOP': 1
            }
        }
        word = generate_word(transitions_dict, 1)
        self.assertEqual(word, 'b')

    def test_second_order_word(self):
        transitions_dict = {
            'START': {
                'START': {
                    'B': 1
                },
                'B': {
                    'UH': 1
                }
            },
            'B': {
                'UH': {
                    'STOP': 1
                }
            },
            'UH': {
                'STOP': {
                    'STOP': 1
                }
            }
        }
        word = generate_word(transitions_dict, 10)
        self.assertEqual(word, 'buh')

class GeneratePhonemeTest(TestCase):
    def test_generate_phoneme(self):
        prior_phones = ['START', 'START']
        transitions_dict = {
            'START': {
                'START': {
                    'B': 1
                }
            }
        }
        phone = _generate_phone(transitions_dict, prior_phones)
        self.assertEqual(phone, 'B')

class EntriesTest(TestCase):
    def test_entries_from_cmudict(self):
        entries = entries_from_cmudict()
        self.assertEqual(
            entries[:2],
            [(u'a', [u'AH0']), (u'a.', [u'EY1'])]
        )

    def test_filtered_entries(self):
        entries = entries_from_cmudict(filt='Austen')
        self.assertEqual(
            entries[:2],
            [(u'a', [u'AH0']), (u'a', [u'EY1'])]
        )

class AustenWordsTest(TestCase):
    def test_austen_words(self):
        words = [word for word in austen_words()]
        words = sorted(words)[-10:]
        self.assertEqual(
            words,
            [
                u'young', u'younger', u'youngest',
                u'your', u'yours', u'yourself', u'youth',
                u'youthful', u'zeal', u'zigzags'
            ]
        )