#!/usr/bin/env python

import glob
import pprint
import xml.dom.minidom

import xmltodict


class SpellNotFoundException(Exception):
    def __init__(self, msg="spell not found"):
        self.message = msg


def remove_learn_action(xml):
    scroll = xml['save']['region']['node']['children']['node']
    actions = scroll['children']['node']['children']['node']
    if type(actions) != list:
        return xml
    for i in range(len(actions)):
        action_block = actions[i]
        action = action_block['attribute']
        # Learn is 33
        if action['@value'] == '33':
            del actions[i]
    return xml


def lock_scroll(scroll_file):
    with open(scroll_file, "r") as fd:
        x = xmltodict.parse(fd.read())

    x = remove_learn_action(x)

    with open(f'{scroll_file}', 'w+') as fd:
       dom = xml.dom.minidom.parseString(xmltodict.unparse(x))
       fd.write(dom.toprettyxml())


if __name__ == "__main__":
    rt_path = "../PAK/Public/SecretScrollsLockClass/RootTemplates/*.lsx"
    for scroll_file in glob.glob(rt_path, recursive=True):
        print(f" [*] {scroll_file}")
        lock_scroll(scroll_file)
