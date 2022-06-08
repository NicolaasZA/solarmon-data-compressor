<?php

include_once "src/db.php";
include_once "src/headers.php";
include_once "src/response.php";
include_once "src/utils.php";

res_cors();

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    die();
}

if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    // ! GET LIST OF FILES
    $db = new DBHelper();
    $db->connect();

    res_json();

    $response = getPayloadObject(Codes::OK);

    $uploadID = (int)read_get_safe('id', 0);

    $response->domain = 'http://data.klausius.co.za/okahandja/';
    if ($uploadID > 0) {
        $response->data = $db->getUpload($uploadID);
    } else {
        $response->data = $db->getUploads();
    }

    echo json_encode($response);
    $db->disconnect();
} else if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $fileToUpload = $_FILES["fileToUpload"];

    res_text();
    if (isset($fileToUpload) != false) {

        $fileSize = $fileToUpload['size'];
        $fileName = $fileToUpload['name'];
        $fileExt = strtolower(pathinfo($fileName, PATHINFO_EXTENSION));

        // Remove extension, prefix and replace _ with -. 
        $fileDate = read_post_safe('date', null);
        if (!isset($fileDate)) {
            $fileDate = str_replace("." . $fileExt, "", str_replace("okahandja-", "", str_replace("_", "-", $fileName)));
        }

        $sourcePath = $fileToUpload['tmp_name'];
        $savePath = 'uploads/okh_' . str_replace("-", "_", $fileDate) . "." . $fileExt;


        if (file_exists($savePath)) {
            echo Codes::FILE_ALREADY_EXISTS;
            die();
        }

        if (move_uploaded_file($sourcePath, $savePath)) {
            $db = new DBHelper();
            $db->connect();
            echo $db->insertUpload($fileName, $fileSize, $fileExt, $savePath, $fileDate);
            $db->disconnect();
        } else {
            echo Codes::FILE_UPLOAD_FAILED;
        }
    } else {
        echo Codes::FILE_NOT_PROVIDED;
    }
} else {
    res_text();
    echo Codes::BAD_REQUEST;
}
