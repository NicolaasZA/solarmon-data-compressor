<?php

/**
 * Read a $_GET field with a fallback value if not set.
 * @return any
 **/
function read_get_safe($fieldName, $fallback)
{
  return isset($_GET[$fieldName]) ? $_GET[$fieldName] : $fallback;
}

/**
 * Read a $_POST field with a fallback value if not set.
 **/
function read_post_safe($fieldName, $fallback)
{
  return isset($_POST[$fieldName]) ? $_POST[$fieldName] : $fallback;
}

/**
 * Read a $_REQUEST field with a fallback value if not set. $_REQUEST contains the aggregate values from both $_GET and $_POST.
 **/
function read_req_safe($fieldName, $fallback)
{
  return isset($_REQUEST[$fieldName]) ? $_REQUEST[$fieldName] : $fallback;
}

function arr_get_safe($arr, $index, $fallback)
{
  if (!is_integer($index) || $index < 0) {
    return $fallback;
  }
  if (!isset($arr) || $index >= count($arr)) {
    return $fallback;
  }
  return $arr[$index];
}
