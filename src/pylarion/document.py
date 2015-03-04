# -*- coding: utf8 -*-
from __future__ import absolute_import, division, print_function
from __future__ import unicode_literals
from pylarion.exceptions import PylarionLibException
import pylarion.base_polarion as bp
import pylarion.enum_option_id as eoi
import pylarion.user as u
import pylarion.subterra_uri as stu
import pylarion.text as t
import pylarion.module_comment as modcom
import pylarion.project as p
import pylarion.custom as custom
import pylarion.signature_context as sigcon
import pylarion.work_item as wi


class Document(bp.BasePolarion):
    '''An object to manage the TestManagement WS tns4:Module '''
    _cls_suds_map = {"allowed_wi_types": {"field_name": "AllowedWITypes",
                                          "is_array": True,
                                          "cls": eoi.EnumOptionId,
                                          "arr_cls": eoi.ArrayOfEnumOptionId,
                                          "inner_field_name":
                                          "eoi.EnumOptionId"},
                     "are_links_from_parent_to_child":
                     "areLinksFromParentToChild",
                     "author": {"field_name": "author", "cls": u.User},
                     "auto_suspect": "autoSuspect",
                     "branched_from": {"field_name": "branchedFrom"},
                     "branched_with_query": "branchedWithQuery",
                     "comments": {"field_name": "comments",
                                  "is_array": True,
                                  "cls": modcom.ModuleComment,
                                  "arr_cls": modcom.ArrayOfModuleComment,
                                  "inner_field_name": "ModuleComment"},
                     "created": "created",
                     "derived_fields": "derived_fields",  # arrayOfstring?
                     "derived_from_uri": {"field_name": "derivedFromURI",
                                          "cls": stu.SubterraURI},
                     "derived_from_link_role": {"field_name":
                                                "derivedFromLinkRole",
                                                "cls": eoi.EnumOptionId},
                     "home_page_content": {"field_name": "homePageContent",
                                           "cls": t.Text},
                     "document_id": "id",
                     "space": "location",
                     "document_absolute_location": "moduleAbsoluteLocation",
                     "document_folder": "moduleFolder",
                     "document_name": "moduleName",
                     "project_id": {"field_name": "project", "cls": p.Project},
                     "signature_contexts": {"field_name": "signatureContexts",
                                            "is_array": True,
                                            "cls": sigcon.SignatureContext,
                                            "arr_cls":
                                            sigcon.ArrayOfSignatureContext,
                                            "inner_field_name":
                                            "SignatureContext"},
                     "status": {"field_name": "status",
                                "cls": eoi.EnumOptionId},
                     "structure_link_role": {"field_name": "structureLinkRole",
                                             "cls": eoi.EnumOptionId},
                     "title": "title",
                     "type": {"field_name": "type", "cls": eoi.EnumOptionId},
                     "updated": "updated",
                     "updated_by": {"field_name": "updatedBy", "cls": u.User},
                     "uses_outline_numbering": "usesOutlineNumbering",
                     "custom_fields": {"field_name": "customFields",
                                       "is_array": True,
                                       "cls": custom.Custom,
                                       "arr_cls": custom.ArrayOfCustom,
                                       "inner_field_name": "Custom"},
                     "uri": "_uri",
                     "_unresolvable": "_unresolvable"}
    _obj_client = "test_management_client"
    _obj_struct = "tns4:Module"
    has_query = True

    @classmethod
    def create(cls, project_id, space, document_name, document_title,
               allowed_wi_types, structure_link_role, home_page_content):
                # There is no document object.
        # don't know what to do with the URI it returns.
        """class method create Creates a document or an old-style
        Module/Document in given location with given parameters.

        Args:
            project_id - project to create module in
            space - document space location with one component or None for
                    default space
            document_name - Document name (required)
            document_title - Document title (required)
            allowed_wi_types - list of types, at least one must be specified
            structure_link_role - required, role which defines the hierarchy of
                                  work items inside the Module
            home_page_content - HTML markup for document home page
        Returns:
            None
        Implements:
            Tracker.createDocument
        """
        if isinstance(allowed_wi_types, str):
            allowed_wi_types = [allowed_wi_types]
        awit = [eoi.EnumOptionId(item)._suds_object
                for item in allowed_wi_types]
        slr = eoi.EnumOptionId(structure_link_role)._suds_object
        uri = cls.session.tracker_client.service.createDocument(
            project_id, space, document_name, document_title, awit,
            slr, home_page_content)
        return Document(uri=uri)

    @classmethod
    def get_documents(cls, project_id, space, fields=[]):
        """returns a list of Document objects
        Args:
            project_id - the project where the modules are located
            space - specific location of the repository
            fields - optional list of fields that should be contained in the
                     returned objects.
        Returns:
            list of Document Objects
        Implements:
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
        for suds_module in getattr(cls.session.tracker_client.service,
                                   function_name)(*parms):
            docs.append(cls(suds_object=suds_module))
        return docs

    @classmethod
    def query(cls, query, is_sql=False, fields=[], sort="document_id",
              limit=-1, baseline_revision=None, query_uris=False):
        """Searches for Modules/Documents.
        Args:
            query - query, either Lucene or SQL
            is_sql (bool), determines if the query is SQL or Lucene
            fields - array of field names to fill in the returned
                     Modules/Documents (can be null). For nested structures in
                     the lists you can use following syntax to include only
                     subset of fields: myList.LIST.key
                     (e.g. linkedWorkItems.LIST.role).
                     For custom fields you can specify which fields you want to
                     be filled using following syntax:
                     customFields.CUSTOM_FIELD_ID (e.g. customFields.risk).
            sort - Lucene sort string (can be null)
            limit - how many results to return (-1 means everything)
            baseline_revision (str) if populated, query done in specified rev
            query_uris - returns a list of URI of the Modules found
        Returns:
            list of modules
        Implements:
            queryModuleUris
            queryModuleUrisBySQL
            queryModuleUrisInBaseline
            queryModuleUrisInBaselineBySQL
            queryModules
            queryModulesBySQL
            queryModulesInBaseline
            queryModulesInBaselineBySQL
        """
        if not query_uris:
            base_name = "queryModules"
        else:
            base_name = "queryModuleUris"
        # calls the parent query function which will build all the required
        # function names and parameter lists generated dynamically based on
        # parameters passed in.
        return super(cls.__class__, cls)._query(
            base_name, query, is_sql, fields=fields, sort=sort, limit=limit,
            baseline_revision=baseline_revision, has_fields=not query_uris)

    def __init__(self, project_id=None, doc_with_space=None, fields=None,
                 uri=None, suds_object=None):
        """constructor for the Module object. Gets the module object from the
        Polarion server based on parameters passed in.
        Args:
            project_id - the project where the module is located
            doc_with_space - specific space/doc_name of the repository,
                    required if project_id is given (Testing, Development, ...)
            fields - optional list of fields that should be contained in the
                     returned object.
            uri - The Polarion specific uri of the module object
            suds_object - the WSDL Module object
        Returns:
            None
        Implements:
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
            self._suds_object = getattr(self.session.tracker_client.service,
                                        function_name)(*parms)

    def _fix_circular_refs(self):
        # a class can't reference itself as a class attribute.
        # defined after instatiation
        self._cls_suds_map["branched_from"]["cls"] = self.__class__

    def create_work_item(self, parent_id, w_item):
        """create a work item in the current document

        Args:
            parent_id - The work_item_id of the parent wi._WorkItem
            wi - The Work Item object to create.
        returns
            The created wi._WorkItem
        """
        self._verify_obj()
        if isinstance(w_item, wi._WorkItem):
            suds_wi = w_item._suds_object
        elif isinstance(w_item, wi._WorkItem()._suds_object.__class__):
            suds_wi = w_item
        else:
            raise PylarionLibException(
                "the w_item parameter must be a _WorkItem")
        parent = wi._WorkItem(work_item_id=parent_id,
                              project_id=self.project_id)
        wi_uri = self.session.tracker_client.service(self.uri, parent.uri,
                                                     suds_wi)
        return wi._WorkItem(uri=wi_uri)

    def delete(self):
        """delete the current document

        Args:
            None
        Returns:
            None
        """
        self._verify_obj()
        self.session.tracker_client.service.deleteModule(self.uri)

    def get_work_items(self, parent_work_item_id, deep, fields):
        """Returns work items (with given fields set) contained in given
        Module/Document under given parent (if specified).

        Args:
            parent_work_item_id (str) - Id of parent work item or null
            deep - true to return work items from the whole subtree
            fields - fields to fill. For nested structures in the lists you can
                     use following syntax to include only subset of fields:
                     myList.LIST.key (e.g. linkedWorkItems.LIST.role).
                     For custom fields you can specify which fields you want to
                     be filled using following syntax:
                     customFields.CUSTOM_FIELD_ID (e.g. customFields.risk).
        Returns:
            list of wi.WorkItem objects
        """
        self._verify_obj()
        parent = wi._WorkItem(work_item_id=parent_work_item_id,
                              project_id=self.project_id)
        p_fields = self._convert_obj_fields_to_polarion(fields)
        suds_wi = self.session.tracker_client.service. \
            getModuleWorkItems(self.uri, parent.uri, deep, p_fields)
        work_items = []
        for w_item in suds_wi:
            work_items.append(wi._WorkItem(suds_object=w_item))
        return work_items

    def update(self):
        """updates the server with the current module data
        Args: None
        Returns: None
        Implements: updateModule
        """
        self.session.tracker_client.service.updateModule(self._suds_object)
