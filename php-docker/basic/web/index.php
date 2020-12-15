<?php

// comment out the following two lines when deployed to production
defined('YII_DEBUG') or define('YII_DEBUG', true);
defined('YII_ENV') or define('YII_ENV', 'dev');

require __DIR__ . '/../vendor/autoload.php';
require __DIR__ . '/../vendor/yiisoft/yii2/Yii.php';

use Jaeger\Config;
use OpenTracing\GlobalTracer;


class OpenTracing
{
    public function __construct()
    {
            $jaeger = new Config(
                [
                    'sampler' => [
                        'type' => 'const',
                        'param' => true,
                    ],
                    'logging' => true,
                    'local_agent' => [
                        'reporting_host' => 'jaeger-collector',
                        'reporting_port' => 14268,
                    ]
                ],
                'test.service'
            );
            $jaeger->initializeTracer();

            $tracer = GlobalTracer::get();

            $parent = $tracer->startActiveSpan('parent');
            sleep(1);
            $child = $tracer->startActiveSpan('child');
            $child->close();
            sleep(3);
            $parent->close();

            $tracer->flush();
    }
}

$config = require __DIR__ . '/../config/web.php';

$jaeger = new OpenTracing();

(new yii\web\Application($config))->run();
