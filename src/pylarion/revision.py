# -*- coding: utf8 -*-
from __future__ import absolute_import, division, print_function
from __future__ import unicode_literals
import suds
import pylarion.base_polarion as bp
import pylarion.subterra_uri as stu


class Revision(bp.BasePolarion):
    """Object to handle the Polarion WSDL tns4:Revision class

    Attributes (for specific details, see Polarion):
        author (string)
        created (dateTime)
        internal_commit (boolean)
        linked_work_item_uris (ArrayOfSubterraURI)
        message (string)
        name (string)
        repository_name (string)
"""
    _cls_suds_map = {"author": "author",
                     "created": "created",
                     "internal_commit": "internalCommit",
                     "linked_work_item_uris": {"field_name":
                                               "linkedWorkItemURIs",
                                               "is_array": True,
                                               "cls": stu.SubterraURI,
                                               "arr_cls":
                                               stu.ArrayOfSubterraURI,
                                               "inner_field_name":
                                               "SubterraURI"},
                     "message": "message",
                     "name": "name",
                     "repository_name": "repositoryName",
                     "uri": "_uri",
                     "_unresolved": "_unresolved"}
    _obj_client = "builder_client"
    _obj_struct = "tns4:Revision"
    has_query = True

    @classmethod
    def query(cls, query, sort="name", fields=[]):
        """Searches revisions

        Args:
            query - query, Lucene
            sort - Lucene sort string (can be null)
            fields - array of field names to fill in the returned
                     Revision (can be null). For nested structures in
                     the lists you can use following syntax to include only
                     subset of fields: myList.LIST.key
                     (e.g. linkedWorkItems.LIST.role).
                     For custom fields you can specify which fields you want to
                     be filled using following syntax:
                     customFields.CUSTOM_FIELD_ID (e.g. customFields.risk).
        Returns:
            list of Revisions
        Implements:
            Tracker.queryRevisions
        """
        return super(cls.__class__, cls)._query("queryRevisions", query,
                                                is_sql=False, fields=fields,
                                                sort=sort, limit=None)


class ArrayOfRevision(bp.BasePolarion):
    _obj_client = "builder_client"
    _obj_struct = "tns4:ArrayOfRevision"
