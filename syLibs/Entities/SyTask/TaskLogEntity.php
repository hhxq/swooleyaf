<?php
/**
 * Created by PhpStorm.
 * User: Administrator
 * Date: 2017-3-5
 * Time: 15:30
 */
namespace Entities\SyTask;

use DB\Entities\MysqlEntity;

class TaskLogEntity extends MysqlEntity {
    public function __construct() {
        parent::__construct('sy_task', 'task_log');
    }

    /**
     * 主键ID
     * @var int
     */
    public $id = null;

    /**
     * 任务标识
     * @var string
     */
    public $tag = '';

    /**
     * 任务结果,json格式
     * @var string
     */
    public $exec_result = '';

    /**
     * 创建时间戳
     * @var int
     */
    public $created = 0;
}