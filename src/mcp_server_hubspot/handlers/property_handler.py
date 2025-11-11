"""
Handler for property-related HubSpot operations.
"""
from typing import Any, Dict, List, Optional
import json

import mcp.types as types

from ..hubspot_client import ApiException
from .base_handler import BaseHandler

class PropertyHandler(BaseHandler):
    """Handler for property-related HubSpot tools."""

    def __init__(self, hubspot_client, faiss_manager, embedding_model):
        """Initialize the property handler.

        Args:
            hubspot_client: HubSpot client
            faiss_manager: FAISS vector store manager
            embedding_model: Sentence transformer model
        """
        super().__init__(hubspot_client, faiss_manager, embedding_model, "property_handler")

    def get_property_schema(self) -> Dict[str, Any]:
        """Get the input schema for getting a property.

        Returns:
            Schema definition dictionary
        """
        return {
            "type": "object",
            "properties": {
                "object_type": {
                    "type": "string",
                    "enum": ["companies", "contacts"],
                    "description": "Type of CRM object"
                },
                "property_name": {
                    "type": "string",
                    "description": "Name of the property"
                }
            },
            "required": ["object_type", "property_name"]
        }

    def get_update_property_schema(self) -> Dict[str, Any]:
        """Get the input schema for updating a property.

        Returns:
            Schema definition dictionary
        """
        return {
            "type": "object",
            "properties": {
                "object_type": {
                    "type": "string",
                    "enum": ["companies", "contacts"],
                    "description": "Type of CRM object"
                },
                "property_name": {
                    "type": "string",
                    "description": "Name of the property"
                },
                "options": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "label": {"type": "string"},
                            "value": {"type": "string"},
                            "description": {"type": "string"},
                            "displayOrder": {"type": "integer"}
                        },
                        "required": ["label", "value"]
                    },
                    "description": "Array of option objects for dropdown fields"
                }
            },
            "required": ["object_type", "property_name", "options"]
        }

    def get_create_property_schema(self) -> Dict[str, Any]:
        """Get the input schema for creating a property.

        Returns:
            Schema definition dictionary
        """
        return {
            "type": "object",
            "properties": {
                "object_type": {
                    "type": "string",
                    "enum": ["companies", "contacts"],
                    "description": "Type of CRM object"
                },
                "name": {
                    "type": "string",
                    "description": "Internal name of the property"
                },
                "label": {
                    "type": "string",
                    "description": "Display label for the property"
                },
                "type": {
                    "type": "string",
                    "description": "Data type (string, number, date, enumeration, etc.)"
                },
                "fieldType": {
                    "type": "string",
                    "description": "Field type (text, textarea, select, number, date, etc.)"
                },
                "groupName": {
                    "type": "string",
                    "description": "Property group name"
                },
                "options": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "label": {"type": "string"},
                            "value": {"type": "string"},
                            "description": {"type": "string"},
                            "displayOrder": {"type": "integer"}
                        },
                        "required": ["label", "value"]
                    },
                    "description": "Array of option objects for dropdown fields"
                },
                "description": {
                    "type": "string",
                    "description": "Property description"
                }
            },
            "required": ["object_type", "name", "label", "type", "fieldType", "groupName"]
        }

    def get_property(self, arguments: Optional[Dict[str, Any]]) -> List[types.TextContent]:
        """Get details of a specific property.

        Args:
            arguments: Tool arguments containing object_type and property_name

        Returns:
            Text response with property definition
        """
        self.validate_required_arguments(arguments, ["object_type", "property_name"])

        object_type = arguments["object_type"]
        property_name = arguments["property_name"]

        results = self.hubspot.get_property(object_type, property_name)

        return self.create_text_response(results)

    def update_property(self, arguments: Optional[Dict[str, Any]]) -> List[types.TextContent]:
        """Update a property definition.

        Args:
            arguments: Tool arguments containing object_type, property_name, and options

        Returns:
            Text response with updated property definition
        """
        self.validate_required_arguments(arguments, ["object_type", "property_name", "options"])

        object_type = arguments["object_type"]
        property_name = arguments["property_name"]
        options = arguments["options"]

        # Extract any additional kwargs
        kwargs = {k: v for k, v in arguments.items()
                 if k not in ["object_type", "property_name", "options"]}

        results = self.hubspot.update_property(object_type, property_name, options, **kwargs)

        return self.create_text_response(results)

    def create_property(self, arguments: Optional[Dict[str, Any]]) -> List[types.TextContent]:
        """Create a new custom property.

        Args:
            arguments: Tool arguments containing property details

        Returns:
            Text response with created property definition
        """
        self.validate_required_arguments(arguments, ["object_type", "name", "label",
                                                     "type", "fieldType", "groupName"])

        object_type = arguments["object_type"]
        name = arguments["name"]
        label = arguments["label"]
        property_type = arguments["type"]
        field_type = arguments["fieldType"]
        group_name = arguments["groupName"]
        options = arguments.get("options")

        # Extract any additional kwargs
        kwargs = {k: v for k, v in arguments.items()
                 if k not in ["object_type", "name", "label", "type",
                            "fieldType", "groupName", "options"]}

        results = self.hubspot.create_property(object_type, name, label, property_type,
                                              field_type, group_name, options, **kwargs)

        return self.create_text_response(results)
