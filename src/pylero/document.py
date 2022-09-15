# -*- coding: utf8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import suds
from pylero._compatible import basestring
from pylero.base_polarion import BasePolarion
from pylero.base_polarion import tx_wrapper
from pylero.custom import ArrayOfCustom
from pylero.custom import Custom
from pylero.enum_option_id import ArrayOfEnumOptionId
from pylero.enum_option_id import EnumOptionId
from pylero.exceptions import PyleroLibException
from pylero.module_comment import ArrayOfModuleComment
from pylero.module_comment import ModuleComment
from pylero.project import Project
from pylero.signature_context import ArrayOfSignatureContext
from pylero.signature_context import SignatureContext
from pylero.subterra_uri import SubterraURI
from pylero.text import Text
from pylero.user import User
from pylero.work_item import _WorkItem


class Document(BasePolarion):
    """An object to manage the TestManagement WS tns4:Module

    Attributes:
        allowed_wi_types (ArrayOfEnumOptionId)
        are_links_from_parent_to_child (boolean)
        author (User)
        auto_suspect (boolean)
        branched_from (Module)
        branched_with_query (string)
        comments (ArrayOfModuleComment)
        created (dateTime)
        custom_fields (ArrayOfCustom)
        derived_fields (ArrayOfstring)
        derived_from_link_role (EnumOptionId)
        derived_from_uri (SubterraURI)
        home_page_content (Text)
        id (string)
        location (Location)
        module_absolute_location (Location)
        module_folder (string)
        module_location (Location)
        module_name (string)
        project (Project)
        signature_contexts (ArrayOfSignatureContext)
        status (EnumOptionId)
        structure_link_role (EnumOptionId)
        title (string)
        type (EnumOptionId)
        updated (dateTime)
        updated_by (User)
        uses_outline_numbering (boolean)"""

    _cls_suds_map = {
        "allowed_wi_types": {
            "field_name": "allowedWITypes",
            "is_array": True,
            "cls": EnumOptionId,
            "arr_cls": ArrayOfEnumOptionId,
            "inner_field_name": "EnumOptionId",
            "enum_id": "workitem-type",
        },
        "are_links_from_parent_to_child": "areLinksFromParentToChild",
        "author": {"field_name": "author", "cls": User},
        "auto_suspect": "autoSuspect",
        "branched_from": {"field_name": "branchedFrom"},  # populated in circ refs
        "branched_with_query": "branchedWithQuery",
        "comments": {
            "field_name": "comments",
            "is_array": True,
            "cls": ModuleComment,
            "arr_cls": ArrayOfModuleComment,
            "inner_field_name": "ModuleComment",
        },
        "created": "created",
        "derived_fields": "derived_fields",  # arrayOfstring?
        "derived_from_uri": {"field_name": "derivedFromURI", "cls": SubterraURI},
        "derived_from_link_role": {
            "field_name": "derivedFromLinkRole",
            "cls": EnumOptionId,
        },
        "home_page_content": {"field_name": "homePageContent", "cls": Text},
        "document_id": "id",
        "space": "moduleLocation",
        "document_absolute_location": "moduleAbsoluteLocation",
        "document_folder": "moduleFolder",
        "document_name": "moduleName",
        "project_id": {"field_name": "project", "cls": Project},
        "signature_contexts": {
            "field_name": "signatureContexts",
            "is_array": True,
            "cls": SignatureContext,
            "arr_cls": ArrayOfSignatureContext,
            "inner_field_name": "SignatureContext",
        },
        "status": {
            "field_name": "status",
            "cls": EnumOptionId,
            "enum_id": "documents/document-status",
        },
        "structure_link_role": {"field_name": "structureLinkRole", "cls": EnumOptionId},
        "title": "title",
        "type": {
            "field_name": "type",
            "cls": EnumOptionId,
            "enum_id": "documents/document-type",
        },
        "updated": "updated",
        "updated_by": {"field_name": "updatedBy", "cls": User},
        "uses_outline_numbering": "usesOutlineNumbering",
        "custom_fields": {
            "field_name": "customFields",
            "is_array": True,
            "cls": Custom,
            "arr_cls": ArrayOfCustom,
            "inner_field_name": "Custom",
        },
        "uri": "_uri",
        "_unresolvable": "_unresolvable",
    }
    _obj_client = "test_management_client"
    _obj_struct = "tns4:Module"
    # The uri struct of a module is different then others because of extra
    # moduleFolder element. Also requires a substitution from # to / and back
    URI_STRUCT = (
        "subterra:data-service:objects:/default/"
        "%(project)s${%(obj)s}{moduleFolder}%(id)s"
    )
    # must wrap lambda with classmethod so it can be used as such
    URI_ID_GET_REPLACE = classmethod(lambda cls, x: x.replace("#", "/"))
    URI_ID_SET_REPLACE = classmethod(lambda cls, x: x.replace("/", "#"))

    @classmethod
    @tx_wrapper
    def create(
        cls,
        project_id,
        space,
        document_name,
        document_title,
        allowed_wi_types,
        document_type,
        structure_link_role="parent",
        home_page_content="",
    ):
        # There is no document object.
        # don't know what to do with the URI it returns.
        """class method create Creates a document or an old-style
        Module/Document in given location with given parameters.

        Args:
            project_id: project to create module in
            space: document space location with one component or None for
                   default space
            document_name: Document name (required)
            document_title: Document title (required)
            allowed_wi_types: list of types, only one should be specified
            document_type: Type of document (required i.e testspecification).
            structure_link_role: required, role which defines the hierarchy of
                                 work items inside the Module, default: parent
            home_page_content: HTML markup for document home page, default ""

        Returns:
            None

        References:
            Tracker.createDocument
        """
        if isinstance(allowed_wi_types, basestring):
            allowed_wi_types = [allowed_wi_types]
        awit = [EnumOptionId(item)._suds_object for item in allowed_wi_types]
        slr = EnumOptionId(structure_link_role)._suds_object
        try:
            uri = cls.session.tracker_client.service.createDocument(
                project_id,
                space,
                document_name,
                document_title,
                awit,
                slr,
                home_page_content,
            )
            doc = Document(uri=uri)
            doc.type = document_type
            # for some reason, when in a tx (@tx_wrapper), the
            # returned doc does not include the home_page_content attribute
            # so it must be reset before the update. If it is not set, an
            # exception is raised:
            # "java.lang.IllegalArgumentException: Content can't be null"
            if not doc.home_page_content:
                doc.home_page_content = home_page_content
            doc.update()
            if not home_page_content:
                # create heading work item for each document
                wi_head = _WorkItem()
                wi_head.type = "heading"
                wi_head.title = document_title
                doc.create_work_item(None, wi_head)
            return doc
        except suds.WebFault as e:
            if "Invalid document on location Location" in e.fault.faultstring:
                raise PyleroLibException(
                    "Document {0}/{1} already exists".format(space, document_name)
                )
            else:
                raise PyleroLibException(e.fault)

    @classmethod
    def get_documents(cls, project_id, space, fields=[]):
        """returns a list of Document objects

        Args:
            project_id: the project where the modules are located
            space: specific location of the repository
            fields: optional list of fields that should be contained in the
                    returned objects.

        Returns:
            list of Document Objects

        References:
            Tracker.getModules
            Tracker.getModulesWithFields
        """
        # function names and parameter lists generated dynamically based on
        # parameters passed in.
        docs = []
        function_name = "getModules"
        parms = [project_id, space]
        p_fields = cls._convert_obj_fields_to_polarion(fields)
        if p_fields:
            function_name += "WithFields"
            parms += [p_fields]
        for suds_module in getattr(cls.session.tracker_client.service, function_name)(
            *parms
        ):
            docs.append(cls(suds_object=suds_module))
        return docs

    @classmethod
    def query(
        cls,
        query,
        is_sql=False,
        fields=["document_id"],
        sort="document_id",
        limit=-1,
        baseline_revision=None,
        query_uris=False,
    ):
        """Searches for Modules/Documents.

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
                    default: list containing "document_id"
            sort: Lucene sort string, default: document_id
            limit: how many results to return (-1 means everything (default))
            baseline_revision (str): if populated, query done in specified rev
                                     default - None
            query_uris: returns a list of URI of the Modules found, instead of
                        a list of Documents. default - False.

        Returns:
            list of modules

        References:
            queryModuleUris
            queryModuleUrisBySQL
            queryModuleUrisInBaseline
            queryModuleUrisInBaselineBySQL
            queryModules
            queryModulesBySQL
            queryModulesInBaseline
            queryModulesInBaselineBySQL
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
            base_name = "queryModules"
        else:
            base_name = "queryModuleUris"
        if baseline_revision:
            base_name += "InBaseline"
        if is_sql:
            base_name += "BySQL"
        docs = getattr(cls.session.tracker_client.service, base_name)(*parms)
        if query_uris:
            return docs
        else:
            lst_doc = [Document(suds_object=doc) for doc in docs]
            return lst_doc

    def __init__(
        self,
        project_id=None,
        doc_with_space=None,
        fields=None,
        uri=None,
        suds_object=None,
    ):
        """constructor for the Module object. Gets the module object from the
        Polarion server based on parameters passed in.

        Args:
            project_id: the project where the module is located
            doc_with_space: specific space/doc_name of the repository,
                            required if project_id is given
                            (Testing, Development, ...)
            fields: optional list of fields that should be contained in the
                     returned object.
            uri: The Polarion specific uri of the module object
            suds_object: the WSDL Module object

        Returns:
            None

        References:
            Tracker.getModuleByLocation
            Tracker.getModuleByLocationWithFields
            Tracker.getModuleByUri
            Tracker.getModuleByUriWithFields
        """
        super(self.__class__, self).__init__(suds_object=suds_object)
        # function names and parameter lists generated dynamically based on
        # parameters passed in.
        if doc_with_space or uri:
            function_name = "getModuleBy"
            parms = []
            if doc_with_space:
                function_name += "Location"
                parms += [project_id, doc_with_space]
            elif uri:
                function_name += "Uri"
                parms.append(uri)
            if fields:
                function_name = "WithFields"
                parms.append(self._convert_obj_fields_to_polarion(fields))
            self._suds_object = getattr(
                self.session.tracker_client.service, function_name
            )(*parms)
            if getattr(self._suds_object, "_unresolvable", True):
                raise PyleroLibException(
                    "The Document {0} was not found.".format(doc_with_space or uri)
                )

    def _fix_circular_refs(self):
        # a class can't reference itself as a class attribute.
        # defined after instatiation
        self._cls_suds_map["branched_from"]["cls"] = self.__class__

    @tx_wrapper
    def create_work_item(self, parent_id, w_item):
        """create a work item in the current document

        Args:
            parent_id: The work_item_id of the parent _WorkItem
            wi: The Work Item object to create.

        Returns:
            The created _WorkItem

        References:
            Tracker.createWorkItemInModule
        """
        self._verify_obj()
        if isinstance(w_item, _WorkItem):
            w_item.verify_required()
            suds_wi = w_item._suds_object
        else:
            raise PyleroLibException("the w_item parameter must be a _WorkItem")
        if parent_id:
            parent_uri = _WorkItem(
                work_item_id=parent_id, project_id=self.project_id
            ).uri
        else:
            doc_wis = self.get_work_items(None, False, None)
            if doc_wis:
                parent_uri = doc_wis[0].uri
            else:
                parent_uri = None
        wi_uri = self.session.tracker_client.service.createWorkItemInModule(
            self.uri, parent_uri, suds_wi
        )
        new_wi = w_item.__class__(uri=wi_uri)
        new_wi._changed_fields = w_item._changed_fields
        new_wi.update()
        new_wi = _WorkItem(uri=wi_uri)
        return new_wi

    def delete(self):
        """delete the current document

        Args:
            None

        Returns:
            None
        """
        self._verify_obj()
        self.session.tracker_client.service.deleteModule(self.uri)

    def get_work_items(
        self, parent_work_item_id, deep, fields=["work_item_id", "type"]
    ):
        """Returns work items (with given fields set) contained in given
        Module/Document under given parent (if specified).

        Args:
            parent_work_item_id (str): Id of parent work item or None
            deep: true to return work items from the whole subtree
            fields: fields to fill. For nested structures in the lists you can
                    use following syntax to include only subset of fields:
                    myList.LIST.key (e.g. linkedWorkItems.LIST.role).
                    For custom fields you can specify which fields you want to
                    be filled using following syntax:
                    customFields.CUSTOM_FIELD_ID (e.g. customFields.risk).

        Returns:
            list of _WorkItem objects

        References:
            Tracker.getModuleWorkItems
        """
        self._verify_obj()
        if parent_work_item_id:
            parent_uri = _WorkItem(
                work_item_id=parent_work_item_id, project_id=self.project_id
            ).uri
        else:
            parent_uri = None
        p_fields = _WorkItem._convert_obj_fields_to_polarion(fields)
        suds_wi = self.session.tracker_client.service.getModuleWorkItems(
            self.uri, parent_uri, deep, p_fields
        )
        work_items = []
        for w_item in suds_wi:
            work_items.append(_WorkItem(suds_object=w_item))
        return work_items

    def move_work_item_here(
        self, work_item_id, parent_id, position=-1, retain_flow=True
    ):
        """Moves a work item to a specific position in a Document. If the work
        item is not yet inside the Document it will be moved into the Document.

        Args:
            work_item_id: WorkItem id to move
            parent_id: The parent WorkItem id, can be None
            position (int): desired position in the list of children or a
                            value < 0 to insert at the end (if the old and new
                            parent is the same then moved work item is not
                            counted)
            retain_flow (bool): true to retain the position of moved work item
                                in the document flow (even if it means to
                                change the parent).
                                false to keep desired parent (even if it means
                                to move work item to different position)

        Returns:
            None

        References:
            Tracker.moveWorkItemToDocument
        """
        self._verify_obj()
        wi = _WorkItem(self.project_id, work_item_id)
        if parent_id:
            parent_uri = _WorkItem(self.project_id, parent_id).uri
        else:
            parent_uri = None
        self.session.tracker_client.service.moveWorkItemToDocument(
            wi.uri, self.uri, parent_uri, position, retain_flow
        )

    def add_referenced_work_item(self, work_item_id):
        """Adds a work item to the document as a referenced work_item to the
        end of the current document.

        Args:
            work_item_id (str): the id of a work item in the same project as
            the current document

        Returns:
            None
        """
        self._verify_obj()
        # verify that the work item passed in exists
        _WorkItem(project_id=self.project_id, work_item_id=work_item_id)
        ref_wi_template = (
            """<div id="polarion_wiki macro name="""
            """module-workitem;params=id=%s|external=true">"""
        )
        self.home_page_content += ref_wi_template % work_item_id
        self.update()

    def update(self):
        """updates the server with the current module data

        Args:
            None

        Returns:
            None

        References:
            Tracker.updateModule
        """
        self.session.tracker_client.service.updateModule(self._suds_object)
