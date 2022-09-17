# -*- coding: utf8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from pylero.base_polarion import BasePolarion
from pylero.project import Project
from pylero.subterra_uri import ArrayOfSubterraURI
from pylero.subterra_uri import SubterraURI
from pylero.text import Text
from pylero.user import User
from pylero.wiki_page_attachment import ArrayOfWikiPageAttachment
from pylero.wiki_page_attachment import WikiPageAttachment


class WikiPage(BasePolarion):
    """Object to handle the Polarion WSDL tns3:WikiPage class

    Attributes:
        attachments (ArrayOfWikiPageAttachment)
        author (User)
        created (dateTime)
        home_page_content (Text)
        wiki_page_id (string)
        linked_page_uris (ArrayOfSubterraURI)
        location (Location)
        page_location (Location)
        page_name (string)
        project (Project)
        space_id (string)
        title (string)
        type (string)
        updated (dateTime)
        updated_by (User)"""

    _cls_suds_map = {
        "attachments": {
            "field_name": "attachments",
            "is_array": True,
            "cls": WikiPageAttachment,
            "arr_cls": ArrayOfWikiPageAttachment,
            "inner_field_name": "WikiPageAttachment",
        },
        "author": {"field_name": "author", "cls": User},
        "created": "created",
        "home_page_content": {"field_name": "homePageContent", "cls": Text},
        "wiki_page_id": "id",
        "linked_page_uris": {
            "field_name": "linkedPageURIs",
            "is_array": True,
            "cls": SubterraURI,
            "arr_cls": ArrayOfSubterraURI,
            "inner_field_name": "SubterraURI",
        },
        "location": "location",
        "page_location": "pageLocation",
        "page_name": "pageName",
        "project": {"field_name": "project", "cls": Project},
        "space_id": "spaceId",
        "title": "title",
        "type": "type",
        "updated": "updated",
        "updated_by": {"field_name": "updatedBy", "cls": User},
        "uri": "_uri",
        "_unresolved": "_unresolved",
    }
    _obj_client = "tracker_client"
    _obj_struct = "tns3:WikiPage"

    @classmethod
    def get_wiki_pages(cls, project_id, space_id, fields):
        """Returns Wiki Pages from given project and space.

        Args:
            project_id: project id (not null)
            space_id: space id (not null)

        Returns:
            list of WikiPage objects
        """
        function_name = "getWikiPages"
        parms = [project_id, space_id]
        if fields:
            function_name += "WithFields"
            parms += [cls._convert_obj_fields_to_polarion(fields)]
        wikis = []
        for suds_wiki in getattr(cls.session.tracker_client.service, function_name)(
            *parms
        ):
            wikis.append(cls(suds_object=suds_wiki))
        return wikis

    @classmethod
    def query(
        cls,
        query,
        is_sql=False,
        fields=["wiki_page_id"],
        sort="wiki_page_id",
        limit=-1,
        baseline_revision=None,
        query_uris=False,
    ):
        """Searches for Wiki Pages .

        Args:
            query: query, either Lucene or SQL
            is_sql (bool): determines if the query is SQL or Lucene
            fields: list of field names to fill in the returned
                     Modules/Documents (can be null). For nested structures in
                     the lists you can use following syntax to include only
                     subset of fields: myList.LIST.key
                     (e.g. linkedWorkItems.LIST.role).
                     For custom fields you can specify which fields you want to
                     be filled using following syntax:
                     customFields.CUSTOM_FIELD_ID (e.g. customFields.risk).
                     default - list containing "wiki_page_id"
            sort: Lucene sort string, default wiki_page_id
            limit: how many results to return (-1 means everything (default))
            baseline_revision (str): if populated, query done in specified rev
                                     default - None
            query_uris: returns a list of URI of the Modules found, instead of
                        a list of WikiPage objects. default - False

        Returns:
            list of modules

        References:
            queryWikiPageUris
            queryWikiPageUrisBySQL
            queryWikiPageUrisInBaseline
            queryWikiPageUrisInBaselineBySQL
            queryWikiPages
            queryWikiPagesBySQL
            queryWikiPagesInBaseline
            queryWikiPagesInBaselineBySQL
        """
        parms = [query]
        # The parameters have to be listed in the specific order, based on the
        # specific function called. That's why there are 2 if not is_sql
        # conditions.
        if not is_sql:
            parms.append(sort)
        if baseline_revision:
            parms.append(baseline_revision)
        if not query_uris:
            p_fields = cls._convert_obj_fields_to_polarion(fields)
            parms.append(p_fields)
        if not is_sql:
            parms.append(limit)
        if not query_uris:
            base_name = "queryWikiPages"
        else:
            base_name = "queryWikiPageUris"
        if baseline_revision:
            base_name += "InBaseline"
        if is_sql:
            base_name += "BySQL"
        wps = getattr(cls.session.tracker_client.service, base_name)(*parms)
        if query_uris:
            return wps
        else:
            lst_wp = [WikiPage(suds_object=wp) for wp in wps]
            return lst_wp

    def __init__(self, fields=None, uri=None, suds_object=None):
        """
        Args:
            fields: list of object fields to be returned in the object

        Returns:
            None

        References:
            Tracker.getWikiPageByUri
            tracker.getWikiPageByUriWithFields
        """
        super(self.__class__, self).__init__(suds_object=suds_object)
        if uri:
            function_name = "getWikiPageByUri"
            parms = [uri]
            if fields:
                function_name += "WithFields"
                parms += [self._convert_obj_fields_to_polarion(fields)]
            self._suds_object = getattr(
                self.session.tracker_client.service, function_name
            )(*parms)
