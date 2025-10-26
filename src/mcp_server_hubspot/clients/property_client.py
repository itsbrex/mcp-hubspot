"""
Client for HubSpot property-related operations.
"""
import json
import logging
from typing import Any, Dict, List, Optional

from hubspot import HubSpot
from hubspot.crm.contacts.exceptions import ApiException

from ..core.formatters import convert_datetime_fields
from ..core.error_handler import handle_hubspot_errors

logger = logging.getLogger('mcp_hubspot_client.property')

class PropertyClient:
    """Client for HubSpot property-related operations."""

    def __init__(self, hubspot_client: HubSpot, access_token: str):
        """Initialize with HubSpot client instance.

        Args:
            hubspot_client: Initialized HubSpot client
            access_token: HubSpot API access token
        """
        self.client = hubspot_client
        self.access_token = access_token

    @handle_hubspot_errors
    def get_property(self, object_type: str, property_name: str) -> str:
        """Get details of a specific property.

        Args:
            object_type: Type of CRM object ("companies" or "contacts")
            property_name: Name of the property

        Returns:
            JSON string with property definition
        """
        # Use the properties API to get property details
        property_response = self.client.crm.properties.core_api.get_by_name(
            object_type=object_type,
            property_name=property_name,
            archived=False
        )

        property_dict = property_response.to_dict()
        converted_property = convert_datetime_fields(property_dict)
        return json.dumps(converted_property)

    @handle_hubspot_errors
    def update_property(self, object_type: str, property_name: str,
                       options: Optional[List[Dict[str, Any]]] = None,
                       **kwargs) -> str:
        """Update a property definition.

        Args:
            object_type: Type of CRM object ("companies" or "contacts")
            property_name: Name of the property
            options: Array of option objects for dropdown fields
            **kwargs: Additional property attributes to update

        Returns:
            JSON string with updated property definition
        """
        from hubspot.crm.properties import PropertyUpdate

        # Build the update object
        update_data = {}

        if options is not None:
            # For dropdown fields, update the options
            update_data['options'] = options

        # Add any other property updates
        for key, value in kwargs.items():
            if key not in ['object_type', 'property_name']:
                update_data[key] = value

        property_update = PropertyUpdate(**update_data)

        # Update the property
        property_response = self.client.crm.properties.core_api.update(
            object_type=object_type,
            property_name=property_name,
            property_update=property_update
        )

        property_dict = property_response.to_dict()
        converted_property = convert_datetime_fields(property_dict)
        return json.dumps(converted_property)

    @handle_hubspot_errors
    def create_property(self, object_type: str, name: str, label: str,
                       property_type: str, field_type: str, group_name: str,
                       options: Optional[List[Dict[str, Any]]] = None,
                       **kwargs) -> str:
        """Create a new custom property.

        Args:
            object_type: Type of CRM object ("companies" or "contacts")
            name: Internal name of the property
            label: Display label for the property
            property_type: Data type (string, number, date, etc.)
            field_type: Field type (text, textarea, select, etc.)
            group_name: Property group name
            options: Array of option objects for dropdown fields
            **kwargs: Additional property attributes

        Returns:
            JSON string with created property definition
        """
        from hubspot.crm.properties import PropertyCreate

        # Build the create object
        create_data = {
            'name': name,
            'label': label,
            'type': property_type,
            'fieldType': field_type,
            'groupName': group_name
        }

        if options is not None:
            create_data['options'] = options

        # Add any other property attributes
        for key, value in kwargs.items():
            if key not in ['object_type', 'name', 'label', 'property_type',
                          'field_type', 'group_name', 'options']:
                create_data[key] = value

        property_create = PropertyCreate(**create_data)

        # Create the property
        property_response = self.client.crm.properties.core_api.create(
            object_type=object_type,
            property_create=property_create
        )

        property_dict = property_response.to_dict()
        converted_property = convert_datetime_fields(property_dict)
        return json.dumps(converted_property)
