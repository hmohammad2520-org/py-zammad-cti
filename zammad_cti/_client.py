import requests
from classmods import ENVMod, logwrap
from typing import Any, Dict, List, Optional

from ._type_aliases import CallDirection, HangupCause

class CTIClient:
    """
    CTIClient provides methods for interacting with the Zammad CTI.

    Zammad CTI Docs: https://docs.zammad.org/en/latest/api/generic-cti/index.html
    """
    @ENVMod.register(section_name='ZammadCTI')
    def __init__(
            self,
            url: str,
            verify_ssl: bool = False,
        ) -> None:
        """
        Initialize CTI Client.

        Args:
            url (str): URL of CTI integrator in Zammad.
            verify_ssl (bool): Verify server's SSL certificate on requests.
        """
        self._url = url
        self._verify_ssl = verify_ssl
        self._session = requests.session()
        self._session.headers['Content-Type'] = 'application/json'


    @logwrap(
        before='Sending HTTP request: args:{args} - kwargs:{kwargs}',
        after=False,
    )
    def _send_request(
            self,
            method: str,
            head_params: Optional[dict] = None,
            get_params: Optional[dict] = None,
            post_params: Optional[dict] = None,
        ) -> Dict[str, Any]:
        """
        Send a request to the Zammad CTI and return the response data.
        For the most part the response is empty unless the call is rejected or blocked in zammad.

        Args:
            request_method (RequestMethod): The HTTP method for the request ('GET', 'POST', etc.).
            head_parms (dict): The headers for the request.
            get_parms (dict): The GET parameters for the request.
            post_params (dict): The POST parameters for the request.
            auto_login (Optional(bool)): Whether to auto login on status code 401, 403.
            caching (bool, optional): Whether to cache the results.
            expire_after (int, optional): The time in seconds to cache the results.

        Returns:
            Dict[str, Any]: JSON Response from server.

        Raises:
            HTTPError: Any server HTTP errors.
        """
        head_params = head_params or {}
        get_params = get_params or {}
        post_params = post_params or {}

        head_params = {k: v for k, v in head_params.items() if v is not None} 
        get_params = {k: v for k, v in get_params.items() if v is not None}
        post_params = {k: v for k, v in post_params.items() if v is not None}

        response: requests.Response = self._session.request(
            method=method,
            url=self._url,
            headers=head_params,
            params=get_params,
            data=post_params,
            verify=self._verify_ssl,
        )
        response.raise_for_status()

        return response.json()


    @logwrap(
        before=False,
        after='Adding new call: {kwargs}, result: {result}',
    )
    def new_call(
            self,
            _from: str,
            to: str,
            direction: CallDirection,
            call_id: str,
            user: Optional[List[str] | str] = None,
            queue: Optional[str] = None,
        ) -> Dict[str, Any]:
        """
        Tell Zammad there's a new call.

        Args:
            _from (str): Number that initiated the call
            to (str): Number that is being called
            direction (CallDirection): The call direction - if your agent initiates a call this will be 'out'
            call_id (str): An ID that is unique for the call. 
                Zammad will use this ID to identify an existing call with following actions 
                (e.g. like answering or hanging up).
            user (Optional[List[str] | str]): The user(s) real name involved. 
                You may have to provide array style ([]) params depending on the call method you choose.
            queue (Optional[str]): An optional queue name, this option is relevant for the Caller Log Filter
        """
        post_params = {
                'event': 'newCall',
                'from': _from,
                'to': to,
                'direction': direction,
                'callId': call_id,
                'user': user,
                'queue': queue,
            }
        post_params = {k: v for k, v in post_params.items() if v is not None}

        return self._send_request(
            method='POST',
            post_params=post_params
        )

    @logwrap(
        before=False,
        after='Changed call state to hangup: {kwargs}, result: {result}',
    )
    def hangup(
            self,
            _from: str,
            to: str,
            direction: CallDirection,
            call_id: str,
            cause: HangupCause,
            answering_number: Optional[str] = None,
        ) -> Dict[str, Any]:
        """
        Tell Zammad that somebody hung up the call.

        Args:
            _from (str): Number that initiated the call
            to (str): Number that is being called
            direction (CallDirection): The call direction - if your agent initiates a call this will be 'out'
            call_id (str): An ID that is unique for the call. 
                Zammad will use this ID to identify an existing call with following actions 
                (e.g. like answering or hanging up).
            cause (HangupCause): This defines the reason of the hangup. 
                Zammad evaluates the cause and indicates e.g. 
                missed calls accordingly in the caller log.
            answering_number (Optional[str]): Zammad will look up for a user with given value, 
                the following attributes will be evaluated in given order: (user.phone, user.login, user.id)
        """
        post_params = {
            'event': 'hangup',
            'from': _from,
            'to': to,
            'direction': direction,
            'callId': call_id,
            'cause': cause,
            'answeringNumber': answering_number,
        }
        post_params = {k: v for k, v in post_params.items() if v is not None}

        return self._send_request(
            method='POST',
            post_params=post_params
        )

    @logwrap(
        before=False,
        after='Changed call state to answer: {kwargs}, result: {result}',
    )
    def answer(
            self,
            _from: str,
            to: str,
            direction: CallDirection,
            call_id: str,
            answering_number: Optional[str] = None,
            user: Optional[List[str] | str] = None,
        ) -> Dict[str, Any]:
        """
        Tell Zammad that someone answered the call.

        Args:
            _from (str): Number that initiated the call
            to (str): Number that is being called
            direction (CallDirection): The call direction - if your agent initiates a call this will be 'out'
            call_id (str): An ID that is unique for the call. 
                Zammad will use this ID to identify an existing call with following actions 
                (e.g. like answering or hanging up).
            answering_number (Optional[str]): Zammad will look up for a user with given value, 
                the following attributes will be evaluated in given order: (user.phone, user.login, user.id)
            user (Optional[List[str] | str]): The user(s) real name involved. 
                You may have to provide array style ([]) params depending on the call method you choose.
        """
        post_params = {
            'event': 'answer',
            'from': _from,
            'to': to,
            'direction': direction,
            'callId': call_id,
            'answeringNumber': answering_number,
            'user': user,
        }
        post_params = {k: v for k, v in post_params.items() if v is not None}

        return self._send_request(
            method='POST',
            post_params=post_params
        )


    def __repr__(self) -> str:
        """
        Provides a string representation for debugging purposes.

        Returns:
            str: A string containing the class name and key attributes.
        """
        return f'{self.__class__.__name__}(url={self._url}), verify_ssl={self._verify_ssl})'


    def __str__(self) -> str:
        """
        Provides a human-readable string representation of the instance.

        Returns:
            str: A simplified string representation of the instance.
        """
        return f'<Zammad CTI Client>'