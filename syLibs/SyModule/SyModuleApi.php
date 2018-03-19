<?php
/**
 * Created by PhpStorm.
 * User: 姜伟
 * Date: 2017/8/22 0022
 * Time: 17:42
 */
namespace SyModule;

use Constant\Server;

class SyModuleApi extends ModuleHttp {
    /**
     * @var \SyModule\SyModuleApi
     */
    private static $instance = null;

    private function __construct() {
        $this->init();
        $this->moduleName = Server::MODULE_BASE_API;
    }

    private function __clone() {
    }

    /**
     * @return \SyModule\SyModuleApi
     */
    public static function getInstance() {
        if(is_null(self::$instance)){
            self::$instance = new self();
        }

        return self::$instance;
    }
}