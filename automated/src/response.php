<?php

class Codes
{
    public const OK = 200;
    public const OK_NO_DATA = 201;
    public const BAD_REQUEST = 402;
    public const INVALID_AUTH = 403;
    public const SQL_NOT_CONNECTED = 404;
    public const INTERNAL_ERROR = 500;

    public const FILE_ALREADY_EXISTS = 1001;
    public const FILE_UPLOAD_FAILED = 1002;
    public const FILE_NOT_PROVIDED = 1003;
}

function getPayloadObject($code)
{
    return (object)array(
        "status" => $code,
    );
}

function getPayloadString($code)
{
    return json_encode(getPayloadObject($code));
}
