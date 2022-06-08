<?php

function res_json()
{
  header('Content-type: application/json; charset=utf-8');
}

function res_text()
{
  header('Content-type: text/plain; charset=utf-8');
}

function res_cors()
{
  header('Access-Control-Allow-Origin: *');
  header('Access-Control-Allow-Headers: content-type');
  header('Access-Control-Allow-Methods: GET, POST, OPTIONS');
}

function res_file($mime, $size, $name)
{
  header("Content-type: $mime");
  header("Content-length: $size");
  header("Content-Disposition: attachment; filename=$name");
}
