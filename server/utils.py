#!/usr/bin/python
#-*- coding=utf-8 -*-

__author__ = ['"wuyadong" <wuyadong@tigerknows.com>']


def unicode2str_for_dict(dictionary):
    """将字典中的unicode类型的字符串换成str
        Args:
            dictionary: 字典
        Returns:
            new_dictionary: 新的字典
    """
    clone_dictionary = {}
    for key, value in dictionary.items():
        key = key if not isinstance(key, unicode) else str(key)
        value = value if not isinstance(value, unicode) else str(value)
        clone_dictionary[key] = value
    return clone_dictionary
