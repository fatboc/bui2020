<?php

namespace app\models;

use yii\db\ActiveRecord;
use yii\OpenTracing;

class Kursy extends ActiveRecord
{
    public static function tableName()
    {
        return 'kursy_prowadzacy';
    }
}
