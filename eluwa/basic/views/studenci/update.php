<?php

use yii\helpers\Html;

/* @var $this yii\web\View */
/* @var $model app\models\Studenci */

$this->title = 'Update Studenci: ' . $model->nr_indeksu;
$this->params['breadcrumbs'][] = ['label' => 'Studencis', 'url' => ['index']];
$this->params['breadcrumbs'][] = ['label' => $model->nr_indeksu, 'url' => ['view', 'id' => $model->nr_indeksu]];
$this->params['breadcrumbs'][] = 'Update';
?>
<div class="studenci-update">

    <h1><?= Html::encode($this->title) ?></h1>

    <?= $this->render('_form', [
        'model' => $model,
    ]) ?>

</div>
