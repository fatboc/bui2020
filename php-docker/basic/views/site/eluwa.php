<?php

require_once __DIR__ . '/../../vendor/autoload.php';

use yii\helpers\Html;
use Jaeger\Config;
use OpenTracing\GlobalTracer;

$config = new Config(
    [
        'sampler' => [
            'type' => Jaeger\SAMPLER_TYPE_CONST,
            'param' => true,
        ],
        'logging' => true,
    ],
    'your-app-name'
);
$config->initializeTracer();

$tracer = GlobalTracer::get();

$scope = $tracer->startActiveSpan('TestSpan', []);
$scope->close();


$tracer->flush();?>

<?= Html::encode('eloooooooo' . date('D d H:i:s'));
?>
