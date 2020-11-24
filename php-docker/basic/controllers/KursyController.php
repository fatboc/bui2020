<?php

namespace app\controllers;

use yii\web\Controller;
use yii\data\Pagination;
use app\models\Kursy;

class KursyController extends Controller
{
    public function actionIndex()
    {
        $query = Kursy::find();

        $pagination = new Pagination([
            'defaultPageSize' => 12,
            'totalCount' => $query->count(),
        ]);

        $kursy = $query->orderBy('nazwa')
                       ->offset($pagination->offset)
                       ->limit($pagination->limit)
                       ->all();

        return $this->render('index', [
            'kursy' => $kursy,
            'pagination' => $pagination,
        ]);
    }
}

