"""
PyDataScouteR - Python client for DataScouteR API
"""
import requests
from typing import List, Dict, Any, Optional
import pandas as pd


class DataScouteRClient:
    """
    Python client for interacting with DataScouteR API
    
    Usage:
        client = DataScouteRClient(api_url="http://localhost:8000")
        result = client.analyze(data)
    """
    
    def __init__(self, api_url: str = "http://localhost:8000", timeout: int = 30):
        """
        Initialize the DataScouteR client
        
        Args:
            api_url: Base URL of the DataScouteR API
            timeout: Request timeout in seconds
        """
        self.api_url = api_url.rstrip('/')
        self.timeout = timeout
        self._session = requests.Session()
    
    def _make_request(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Internal method to make API requests"""
        url = f"{self.api_url}/{endpoint.lstrip('/')}"
        
        try:
            response = self._session.post(url, json=data, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"API request failed: {str(e)}")
    
    def health_check(self) -> Dict[str, Any]:
        """Check if the API is healthy and running"""
        try:
            response = self._session.get(f"{self.api_url}/health", timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Health check failed: {str(e)}")
    
    def get_gk(self) -> pd.DataFrame:
        """
        Get goalkeeper data from DataScouteR
        
        Returns:
            Pandas DataFrame containing goalkeeper statistics
        """
        try:
            response = self._session.get(f"{self.api_url}/gk", timeout=self.timeout)
            response.raise_for_status()
            data = response.json()
            
            if not data.get('success'):
                raise Exception(f"Failed to get goalkeeper data: {data.get('message', 'Unknown error')}")
            
            # Convert list of dicts back to DataFrame
            result = data.get('result')
            return pd.DataFrame(result)
        
        except requests.exceptions.RequestException as e:
            raise Exception(f"API request failed: {str(e)}")
    
    def get_fw(self) -> pd.DataFrame:
        """
        Get forward player data from DataScouteR
        
        Returns:
            Pandas DataFrame containing forward player statistics
        """
        try:
            response = self._session.get(f"{self.api_url}/fw", timeout=self.timeout)
            response.raise_for_status()
            data = response.json()
            
            if not data.get('success'):
                raise Exception(f"Failed to get forward data: {data.get('message', 'Unknown error')}")
            
            # Convert list of dicts back to DataFrame
            result = data.get('result')
            return pd.DataFrame(result)
        
        except requests.exceptions.RequestException as e:
            raise Exception(f"API request failed: {str(e)}")
    
    def close(self):
        """Close the session"""
        self._session.close()
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()


# Convenience functions for quick usage
def get_goalkeepers(api_url: str = "http://localhost:8000") -> pd.DataFrame:
    """
    Convenience function to get goalkeeper data without creating a client instance
    
    Args:
        api_url: Base URL of the DataScouteR API
        
    Returns:
        Pandas DataFrame containing goalkeeper statistics
    """
    with DataScouteRClient(api_url=api_url) as client:
        return client.get_gk()


def get_forwards(api_url: str = "http://localhost:8000") -> pd.DataFrame:
    """
    Convenience function to get forward data without creating a client instance
    
    Args:
        api_url: Base URL of the DataScouteR API
        
    Returns:
        Pandas DataFrame containing forward player statistics
    """
    with DataScouteRClient(api_url=api_url) as client:
        return client.get_fw()