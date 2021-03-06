from __future__ import print_function

from lxml import etree

import re

from fontaine.ext.base import BaseExt
import os


class Extension(BaseExt):

    extension_name = 'extensis'

    @staticmethod
    def __getcharmaps__():
        glyphs = {}
        for ext in Extension.get_codepoints():
            parent_name = ext.getparent().attrib.get('parent')

            common_name = u'Extensis %s' % ext.getparent().attrib['name']
            unicodes = []
            if parent_name:
                common_name += u' + ' + parent_name
                unicodes = glyphs.get(parent_name, [])
            unicodes += Extension.get_unicodes(ext)
            glyphs[ext.getparent().attrib['name']] = unicodes

            abbr = ext.getparent().attrib['abbreviated-name']

            yield type('Charmap', (object,),
                       dict(glyphs=unicodes, common_name=common_name,
                            native_name='', abbreviation=abbr))

    @staticmethod
    def get_codepoints():
        """ Return all XML <scanning-codepoints> in received XML """
        # response = requests.get(EXTENSIS_LANG_XML)
        # if response.status_code != 200:
        #     return []

        xml_content = open(os.path.join(os.path.dirname(__file__), 'languages.xml'), 'r').read()

        content = re.sub('<!--.[^>]*-->', '', xml_content)

        doc = etree.fromstring(content.lstrip('`'))
        return doc.findall('.//scanning-codepoints')

    @staticmethod
    def get_unicodes(codepoint):
        """ Return list of unicodes for <scanning-codepoints> """
        result = re.sub('\s', '', codepoint.text)
        return Extension.convert_to_list_of_unicodes(result)
