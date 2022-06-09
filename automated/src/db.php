<?php

require_once 'src/conf.php';
require_once 'src/response.php';

class DBHelper
{
    private ?PDO $conn = null;
    private bool $connected = false;
    public ?string $err = null;

    // ! CONNECTIVITY
    // ! CONNECTIVITY
    // ! CONNECTIVITY

    public function connect()
    {
        try {
            $this->conn = new PDO(DBConfig::DSN, DBConfig::USR, DBConfig::PWD);
            $this->conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
            $this->err = null;

            $this->connected = true;
            return true;
        } catch (Exception $exc) {
            $this->err = $exc->getMessage();
            $this->connected = false;
            return false;
        }
    }

    public function disconnect()
    {
        $this->conn = null;
        $this->connected = false;
    }

    public function isConnected()
    {
        return $this->connected == true;
    }

    // ! WRAPPERS
    // ! WRAPPERS
    // ! WRAPPERS

    /**
     * Perform an SELECT query. Returns resulting records as objects. (PDO::FETCH_OBJ)
     */
    public function select($sql)
    {
        if ($this->isConnected()) {
            $stm = $this->conn->query($sql);
            return $stm->fetchAll(PDO::FETCH_OBJ);
        } else {
            throw new PDOException("Not connected to database. Call connect() first.");
        }
    }

    /**
     * Perform an SELECT query. Returns resulting records as arrays, indexed by column select order. (PDO::FETCH_OBJ)
     */
    public function selectArr($sql)
    {
        if ($this->isConnected()) {
            $stm = $this->conn->query($sql);
            return $stm->fetchAll(PDO::FETCH_NUM);
        } else {
            throw new PDOException("Not connected to database. Call connect() first.");
        }
    }

    /**
     * Perform an INSERT query. Returns true if the query was executed.
     */
    public function insert($sql)
    {
        if ($this->isConnected()) {
            $this->conn->exec($sql);
            return $this->conn->lastInsertId();
        } else {
            throw new PDOException("Not connected to database. Call connect() first.");
        }
    }

    /**
     * Perform an INSERT query. Returns the number of rows that were modified or deleted by the SQL statement you issued..
     */
    public function insertCount($sql)
    {
        if ($this->isConnected()) {
            $count = $this->conn->exec($sql);
            return $count;
        } else {
            throw new PDOException("Not connected to database. Call connect() first.");
        }
    }

    /**
     * Perform an UPDATE query. Returns the amount of affected rows.
     */
    public function update($sql)
    {
        if ($this->isConnected()) {
            $stm = $this->conn->prepare($sql);
            $stm->execute();
            return $stm->rowCount();
        } else {
            throw new PDOException("Not connected to database. Call connect() first.");
        }
    }

    // ! UPLOADS
    // ! UPLOADS
    // ! UPLOADS

    public function getUpload($uploadID)
    {
        if ($this->isConnected()) {
            $sth = $this->conn->prepare('SELECT * FROM okh_files WHERE id = :uploadID');
            if ($sth == false) {
                return Codes::INTERNAL_ERROR;
            }

            $sth->execute(array(
                'uploadID' => $uploadID,
            ));

            $results = $sth->fetchAll(PDO::FETCH_ASSOC);
            if ($results != false && count($results) > 0) {
                return $results[0];
            } else {
                return null;
            }
        } else {
            throw new PDOException("Not connected to database. Call connect() first.");
        }
    }

    public function getUploads()
    {
        if ($this->isConnected()) {
            $sth = $this->conn->prepare('SELECT id,fdate,fpath,0 as records FROM okh_files');
            if ($sth == false) {
                return Codes::INTERNAL_ERROR;
            }

            $sth->execute();

            $results = $sth->fetchAll(PDO::FETCH_ASSOC);
            if ($results != false) {
                return $results;
            } else {
                return null;
            }
        } else {
            return null;
        }
    }

    public function insertUpload($fName, $fSize, $fType, $fPath, $fDate)
    {
        if ($this->isConnected()) {
            $sth = $this->conn->prepare("INSERT INTO okh_files (fname, fsize, ftype, fpath, fdate) VALUES (:fName, :fSize, :fType, :fPath, :fDate)");
            if ($sth == false) {
                return Codes::FILE_UPLOAD_FAILED;
            }

            $sth->execute(array(
                'fName' => $fName,
                'fSize' => $fSize,
                'fType' => $fType,
                'fPath' => $fPath,
                'fDate' => $fDate
            ));

            return Codes::OK;
        } else {
            return Codes::SQL_NOT_CONNECTED;
        }
    }
}
