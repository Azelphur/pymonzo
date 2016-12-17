# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from abc import ABCMeta

import dateutil.parser
from six import with_metaclass


class MonzoObject(object, with_metaclass(ABCMeta)):
    """
    Base abstract class for Monzo API objects
    """
    _required_keys = []

    def __init__(self, data):
        """
        Takes JSON data and maps the keys as class properties, while also
        requiring certain keys to be present to make sure we got the response
        we wanted.

        :param data: JSON data from appropriate Monzo API request
        :type data: dict
        """
        if not all(k in data for k in self._required_keys):
            raise ValueError("Passed data doesn't have all required keys")

        self._data = data


class MonzoAccount(MonzoObject):
    """
    Class representation of Monzo account
    """
    _required_keys = ['id', 'description', 'created']

    def __init__(self, data):
        """
        Takes JSON data and maps the keys as class properties, while also
        requiring certain keys to be present to make sure we got the response
        we wanted.

        :param data: JSON data from appropriate Monzo API request
        :type data: dict
        """
        super(MonzoAccount, self).__init__(data)

        # Take care of non-usual fields
        self.created = dateutil.parser.parse(data.pop('created'))

        # Map the rest of the fields automatically
        self.__dict__.update(**data)


class MonzoBalance(MonzoObject):
    """
    Class representation of Monzo account balance
    """
    _required_keys = ['balance', 'currency', 'spend_today']

    def __init__(self, data):
        """
        Takes JSON data and maps the keys as class properties, while also
        requiring certain keys to be present to make sure we got the response
        we wanted.

        :param data: JSON data from appropriate Monzo API request
        :type data: dict
        """
        super(MonzoBalance, self).__init__(data)

        # Map all the fields automatically
        self.__dict__.update(**data)


class MonzoTransaction(MonzoObject):
    """
    Class representation of Monzo transaction
    """
    _required_keys = [
        'account_balance', 'amount', 'created', 'currency',
        'description', 'id', 'merchant', 'metadata', 'notes',
        'is_load', 'category',
    ]

    def __init__(self, data):
        """
        Takes JSON data and maps the keys as class properties, while also
        requiring certain keys to be present to make sure we got the response
        we wanted.

        :param data: JSON data from appropriate Monzo API request
        :type data: dict
        """
        super(MonzoTransaction, self).__init__(data)

        # Take care of non-usual fields
        self.created = dateutil.parser.parse(data.pop('created'))

        if data.get('settled'):  # Not always returned
            self.settled = dateutil.parser.parse(data.pop('settled'))

        # Merchant field can contain either merchant ID or the whole object
        if data.get('merchant') and not isinstance(data['merchant'], str):
            self.merchant = MonzoMerchant(data=data.pop('merchant'))

        # Map the rest of the fields automatically
        self.__dict__.update(**data)


class MonzoMerchant(MonzoObject):
    """
    Class representation of Monzo merchants
    """
    _required_keys = [
        'address', 'created', 'group_id', 'id',
        'logo', 'emoji', 'name', 'category',
    ]

    def __init__(self, data):
        """
        Takes JSON data and maps the keys as class properties, while also
        requiring certain keys to be present to make sure we got the response
        we wanted.

        :param data: JSON data from appropriate Monzo API request
        :type data: dict
        """
        super(MonzoMerchant, self).__init__(data)

        # Take care of non-usual fields
        self.created = dateutil.parser.parse(data.pop('created'))

        # Map the rest of the fields automatically
        self.__dict__.update(**data)
