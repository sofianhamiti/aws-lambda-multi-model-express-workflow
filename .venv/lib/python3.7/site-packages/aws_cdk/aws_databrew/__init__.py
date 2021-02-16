"""
# AWS::DataBrew Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_databrew as databrew
```
"""
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from ._jsii import *

import aws_cdk.core


@jsii.implements(aws_cdk.core.IInspectable)
class CfnDataset(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-databrew.CfnDataset",
):
    """A CloudFormation ``AWS::DataBrew::Dataset``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-dataset.html
    :cloudformationResource: AWS::DataBrew::Dataset
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        input: typing.Any,
        name: builtins.str,
        format_options: typing.Any = None,
        tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]] = None,
    ) -> None:
        """Create a new ``AWS::DataBrew::Dataset``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param input: ``AWS::DataBrew::Dataset.Input``.
        :param name: ``AWS::DataBrew::Dataset.Name``.
        :param format_options: ``AWS::DataBrew::Dataset.FormatOptions``.
        :param tags: ``AWS::DataBrew::Dataset.Tags``.
        """
        props = CfnDatasetProps(
            input=input, name=name, format_options=format_options, tags=tags
        )

        jsii.create(CfnDataset, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        """(experimental) Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        """``AWS::DataBrew::Dataset.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-dataset.html#cfn-databrew-dataset-tags
        """
        return jsii.get(self, "tags")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="formatOptions")
    def format_options(self) -> typing.Any:
        """``AWS::DataBrew::Dataset.FormatOptions``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-dataset.html#cfn-databrew-dataset-formatoptions
        """
        return jsii.get(self, "formatOptions")

    @format_options.setter # type: ignore
    def format_options(self, value: typing.Any) -> None:
        jsii.set(self, "formatOptions", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="input")
    def input(self) -> typing.Any:
        """``AWS::DataBrew::Dataset.Input``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-dataset.html#cfn-databrew-dataset-input
        """
        return jsii.get(self, "input")

    @input.setter # type: ignore
    def input(self, value: typing.Any) -> None:
        jsii.set(self, "input", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        """``AWS::DataBrew::Dataset.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-dataset.html#cfn-databrew-dataset-name
        """
        return jsii.get(self, "name")

    @name.setter # type: ignore
    def name(self, value: builtins.str) -> None:
        jsii.set(self, "name", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-databrew.CfnDatasetProps",
    jsii_struct_bases=[],
    name_mapping={
        "input": "input",
        "name": "name",
        "format_options": "formatOptions",
        "tags": "tags",
    },
)
class CfnDatasetProps:
    def __init__(
        self,
        *,
        input: typing.Any,
        name: builtins.str,
        format_options: typing.Any = None,
        tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]] = None,
    ) -> None:
        """Properties for defining a ``AWS::DataBrew::Dataset``.

        :param input: ``AWS::DataBrew::Dataset.Input``.
        :param name: ``AWS::DataBrew::Dataset.Name``.
        :param format_options: ``AWS::DataBrew::Dataset.FormatOptions``.
        :param tags: ``AWS::DataBrew::Dataset.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-dataset.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "input": input,
            "name": name,
        }
        if format_options is not None:
            self._values["format_options"] = format_options
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def input(self) -> typing.Any:
        """``AWS::DataBrew::Dataset.Input``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-dataset.html#cfn-databrew-dataset-input
        """
        result = self._values.get("input")
        assert result is not None, "Required property 'input' is missing"
        return result

    @builtins.property
    def name(self) -> builtins.str:
        """``AWS::DataBrew::Dataset.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-dataset.html#cfn-databrew-dataset-name
        """
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return result

    @builtins.property
    def format_options(self) -> typing.Any:
        """``AWS::DataBrew::Dataset.FormatOptions``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-dataset.html#cfn-databrew-dataset-formatoptions
        """
        result = self._values.get("format_options")
        return result

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        """``AWS::DataBrew::Dataset.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-dataset.html#cfn-databrew-dataset-tags
        """
        result = self._values.get("tags")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDatasetProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnJob(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-databrew.CfnJob",
):
    """A CloudFormation ``AWS::DataBrew::Job``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-job.html
    :cloudformationResource: AWS::DataBrew::Job
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        role_arn: builtins.str,
        type: builtins.str,
        dataset_name: typing.Optional[builtins.str] = None,
        encryption_key_arn: typing.Optional[builtins.str] = None,
        encryption_mode: typing.Optional[builtins.str] = None,
        log_subscription: typing.Optional[builtins.str] = None,
        max_capacity: typing.Optional[jsii.Number] = None,
        max_retries: typing.Optional[jsii.Number] = None,
        output_location: typing.Any = None,
        outputs: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnJob.OutputProperty"]]]] = None,
        project_name: typing.Optional[builtins.str] = None,
        recipe: typing.Any = None,
        tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]] = None,
        timeout: typing.Optional[jsii.Number] = None,
    ) -> None:
        """Create a new ``AWS::DataBrew::Job``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: ``AWS::DataBrew::Job.Name``.
        :param role_arn: ``AWS::DataBrew::Job.RoleArn``.
        :param type: ``AWS::DataBrew::Job.Type``.
        :param dataset_name: ``AWS::DataBrew::Job.DatasetName``.
        :param encryption_key_arn: ``AWS::DataBrew::Job.EncryptionKeyArn``.
        :param encryption_mode: ``AWS::DataBrew::Job.EncryptionMode``.
        :param log_subscription: ``AWS::DataBrew::Job.LogSubscription``.
        :param max_capacity: ``AWS::DataBrew::Job.MaxCapacity``.
        :param max_retries: ``AWS::DataBrew::Job.MaxRetries``.
        :param output_location: ``AWS::DataBrew::Job.OutputLocation``.
        :param outputs: ``AWS::DataBrew::Job.Outputs``.
        :param project_name: ``AWS::DataBrew::Job.ProjectName``.
        :param recipe: ``AWS::DataBrew::Job.Recipe``.
        :param tags: ``AWS::DataBrew::Job.Tags``.
        :param timeout: ``AWS::DataBrew::Job.Timeout``.
        """
        props = CfnJobProps(
            name=name,
            role_arn=role_arn,
            type=type,
            dataset_name=dataset_name,
            encryption_key_arn=encryption_key_arn,
            encryption_mode=encryption_mode,
            log_subscription=log_subscription,
            max_capacity=max_capacity,
            max_retries=max_retries,
            output_location=output_location,
            outputs=outputs,
            project_name=project_name,
            recipe=recipe,
            tags=tags,
            timeout=timeout,
        )

        jsii.create(CfnJob, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        """(experimental) Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        """``AWS::DataBrew::Job.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-job.html#cfn-databrew-job-tags
        """
        return jsii.get(self, "tags")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        """``AWS::DataBrew::Job.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-job.html#cfn-databrew-job-name
        """
        return jsii.get(self, "name")

    @name.setter # type: ignore
    def name(self, value: builtins.str) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="outputLocation")
    def output_location(self) -> typing.Any:
        """``AWS::DataBrew::Job.OutputLocation``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-job.html#cfn-databrew-job-outputlocation
        """
        return jsii.get(self, "outputLocation")

    @output_location.setter # type: ignore
    def output_location(self, value: typing.Any) -> None:
        jsii.set(self, "outputLocation", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="recipe")
    def recipe(self) -> typing.Any:
        """``AWS::DataBrew::Job.Recipe``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-job.html#cfn-databrew-job-recipe
        """
        return jsii.get(self, "recipe")

    @recipe.setter # type: ignore
    def recipe(self, value: typing.Any) -> None:
        jsii.set(self, "recipe", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        """``AWS::DataBrew::Job.RoleArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-job.html#cfn-databrew-job-rolearn
        """
        return jsii.get(self, "roleArn")

    @role_arn.setter # type: ignore
    def role_arn(self, value: builtins.str) -> None:
        jsii.set(self, "roleArn", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        """``AWS::DataBrew::Job.Type``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-job.html#cfn-databrew-job-type
        """
        return jsii.get(self, "type")

    @type.setter # type: ignore
    def type(self, value: builtins.str) -> None:
        jsii.set(self, "type", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="datasetName")
    def dataset_name(self) -> typing.Optional[builtins.str]:
        """``AWS::DataBrew::Job.DatasetName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-job.html#cfn-databrew-job-datasetname
        """
        return jsii.get(self, "datasetName")

    @dataset_name.setter # type: ignore
    def dataset_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "datasetName", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="encryptionKeyArn")
    def encryption_key_arn(self) -> typing.Optional[builtins.str]:
        """``AWS::DataBrew::Job.EncryptionKeyArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-job.html#cfn-databrew-job-encryptionkeyarn
        """
        return jsii.get(self, "encryptionKeyArn")

    @encryption_key_arn.setter # type: ignore
    def encryption_key_arn(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "encryptionKeyArn", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="encryptionMode")
    def encryption_mode(self) -> typing.Optional[builtins.str]:
        """``AWS::DataBrew::Job.EncryptionMode``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-job.html#cfn-databrew-job-encryptionmode
        """
        return jsii.get(self, "encryptionMode")

    @encryption_mode.setter # type: ignore
    def encryption_mode(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "encryptionMode", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="logSubscription")
    def log_subscription(self) -> typing.Optional[builtins.str]:
        """``AWS::DataBrew::Job.LogSubscription``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-job.html#cfn-databrew-job-logsubscription
        """
        return jsii.get(self, "logSubscription")

    @log_subscription.setter # type: ignore
    def log_subscription(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "logSubscription", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="maxCapacity")
    def max_capacity(self) -> typing.Optional[jsii.Number]:
        """``AWS::DataBrew::Job.MaxCapacity``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-job.html#cfn-databrew-job-maxcapacity
        """
        return jsii.get(self, "maxCapacity")

    @max_capacity.setter # type: ignore
    def max_capacity(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "maxCapacity", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="maxRetries")
    def max_retries(self) -> typing.Optional[jsii.Number]:
        """``AWS::DataBrew::Job.MaxRetries``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-job.html#cfn-databrew-job-maxretries
        """
        return jsii.get(self, "maxRetries")

    @max_retries.setter # type: ignore
    def max_retries(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "maxRetries", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="outputs")
    def outputs(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnJob.OutputProperty"]]]]:
        """``AWS::DataBrew::Job.Outputs``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-job.html#cfn-databrew-job-outputs
        """
        return jsii.get(self, "outputs")

    @outputs.setter # type: ignore
    def outputs(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnJob.OutputProperty"]]]],
    ) -> None:
        jsii.set(self, "outputs", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="projectName")
    def project_name(self) -> typing.Optional[builtins.str]:
        """``AWS::DataBrew::Job.ProjectName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-job.html#cfn-databrew-job-projectname
        """
        return jsii.get(self, "projectName")

    @project_name.setter # type: ignore
    def project_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "projectName", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="timeout")
    def timeout(self) -> typing.Optional[jsii.Number]:
        """``AWS::DataBrew::Job.Timeout``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-job.html#cfn-databrew-job-timeout
        """
        return jsii.get(self, "timeout")

    @timeout.setter # type: ignore
    def timeout(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "timeout", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-databrew.CfnJob.OutputProperty",
        jsii_struct_bases=[],
        name_mapping={
            "location": "location",
            "compression_format": "compressionFormat",
            "format": "format",
            "overwrite": "overwrite",
            "partition_columns": "partitionColumns",
        },
    )
    class OutputProperty:
        def __init__(
            self,
            *,
            location: typing.Union[aws_cdk.core.IResolvable, "CfnJob.S3LocationProperty"],
            compression_format: typing.Optional[builtins.str] = None,
            format: typing.Optional[builtins.str] = None,
            overwrite: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
            partition_columns: typing.Optional[typing.List[builtins.str]] = None,
        ) -> None:
            """
            :param location: ``CfnJob.OutputProperty.Location``.
            :param compression_format: ``CfnJob.OutputProperty.CompressionFormat``.
            :param format: ``CfnJob.OutputProperty.Format``.
            :param overwrite: ``CfnJob.OutputProperty.Overwrite``.
            :param partition_columns: ``CfnJob.OutputProperty.PartitionColumns``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-job-output.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "location": location,
            }
            if compression_format is not None:
                self._values["compression_format"] = compression_format
            if format is not None:
                self._values["format"] = format
            if overwrite is not None:
                self._values["overwrite"] = overwrite
            if partition_columns is not None:
                self._values["partition_columns"] = partition_columns

        @builtins.property
        def location(
            self,
        ) -> typing.Union[aws_cdk.core.IResolvable, "CfnJob.S3LocationProperty"]:
            """``CfnJob.OutputProperty.Location``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-job-output.html#cfn-databrew-job-output-location
            """
            result = self._values.get("location")
            assert result is not None, "Required property 'location' is missing"
            return result

        @builtins.property
        def compression_format(self) -> typing.Optional[builtins.str]:
            """``CfnJob.OutputProperty.CompressionFormat``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-job-output.html#cfn-databrew-job-output-compressionformat
            """
            result = self._values.get("compression_format")
            return result

        @builtins.property
        def format(self) -> typing.Optional[builtins.str]:
            """``CfnJob.OutputProperty.Format``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-job-output.html#cfn-databrew-job-output-format
            """
            result = self._values.get("format")
            return result

        @builtins.property
        def overwrite(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
            """``CfnJob.OutputProperty.Overwrite``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-job-output.html#cfn-databrew-job-output-overwrite
            """
            result = self._values.get("overwrite")
            return result

        @builtins.property
        def partition_columns(self) -> typing.Optional[typing.List[builtins.str]]:
            """``CfnJob.OutputProperty.PartitionColumns``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-job-output.html#cfn-databrew-job-output-partitioncolumns
            """
            result = self._values.get("partition_columns")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OutputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-databrew.CfnJob.S3LocationProperty",
        jsii_struct_bases=[],
        name_mapping={"bucket": "bucket", "key": "key"},
    )
    class S3LocationProperty:
        def __init__(
            self,
            *,
            bucket: builtins.str,
            key: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param bucket: ``CfnJob.S3LocationProperty.Bucket``.
            :param key: ``CfnJob.S3LocationProperty.Key``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-job-s3location.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "bucket": bucket,
            }
            if key is not None:
                self._values["key"] = key

        @builtins.property
        def bucket(self) -> builtins.str:
            """``CfnJob.S3LocationProperty.Bucket``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-job-s3location.html#cfn-databrew-job-s3location-bucket
            """
            result = self._values.get("bucket")
            assert result is not None, "Required property 'bucket' is missing"
            return result

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            """``CfnJob.S3LocationProperty.Key``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-job-s3location.html#cfn-databrew-job-s3location-key
            """
            result = self._values.get("key")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3LocationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-databrew.CfnJobProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "role_arn": "roleArn",
        "type": "type",
        "dataset_name": "datasetName",
        "encryption_key_arn": "encryptionKeyArn",
        "encryption_mode": "encryptionMode",
        "log_subscription": "logSubscription",
        "max_capacity": "maxCapacity",
        "max_retries": "maxRetries",
        "output_location": "outputLocation",
        "outputs": "outputs",
        "project_name": "projectName",
        "recipe": "recipe",
        "tags": "tags",
        "timeout": "timeout",
    },
)
class CfnJobProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        role_arn: builtins.str,
        type: builtins.str,
        dataset_name: typing.Optional[builtins.str] = None,
        encryption_key_arn: typing.Optional[builtins.str] = None,
        encryption_mode: typing.Optional[builtins.str] = None,
        log_subscription: typing.Optional[builtins.str] = None,
        max_capacity: typing.Optional[jsii.Number] = None,
        max_retries: typing.Optional[jsii.Number] = None,
        output_location: typing.Any = None,
        outputs: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnJob.OutputProperty]]]] = None,
        project_name: typing.Optional[builtins.str] = None,
        recipe: typing.Any = None,
        tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]] = None,
        timeout: typing.Optional[jsii.Number] = None,
    ) -> None:
        """Properties for defining a ``AWS::DataBrew::Job``.

        :param name: ``AWS::DataBrew::Job.Name``.
        :param role_arn: ``AWS::DataBrew::Job.RoleArn``.
        :param type: ``AWS::DataBrew::Job.Type``.
        :param dataset_name: ``AWS::DataBrew::Job.DatasetName``.
        :param encryption_key_arn: ``AWS::DataBrew::Job.EncryptionKeyArn``.
        :param encryption_mode: ``AWS::DataBrew::Job.EncryptionMode``.
        :param log_subscription: ``AWS::DataBrew::Job.LogSubscription``.
        :param max_capacity: ``AWS::DataBrew::Job.MaxCapacity``.
        :param max_retries: ``AWS::DataBrew::Job.MaxRetries``.
        :param output_location: ``AWS::DataBrew::Job.OutputLocation``.
        :param outputs: ``AWS::DataBrew::Job.Outputs``.
        :param project_name: ``AWS::DataBrew::Job.ProjectName``.
        :param recipe: ``AWS::DataBrew::Job.Recipe``.
        :param tags: ``AWS::DataBrew::Job.Tags``.
        :param timeout: ``AWS::DataBrew::Job.Timeout``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-job.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "name": name,
            "role_arn": role_arn,
            "type": type,
        }
        if dataset_name is not None:
            self._values["dataset_name"] = dataset_name
        if encryption_key_arn is not None:
            self._values["encryption_key_arn"] = encryption_key_arn
        if encryption_mode is not None:
            self._values["encryption_mode"] = encryption_mode
        if log_subscription is not None:
            self._values["log_subscription"] = log_subscription
        if max_capacity is not None:
            self._values["max_capacity"] = max_capacity
        if max_retries is not None:
            self._values["max_retries"] = max_retries
        if output_location is not None:
            self._values["output_location"] = output_location
        if outputs is not None:
            self._values["outputs"] = outputs
        if project_name is not None:
            self._values["project_name"] = project_name
        if recipe is not None:
            self._values["recipe"] = recipe
        if tags is not None:
            self._values["tags"] = tags
        if timeout is not None:
            self._values["timeout"] = timeout

    @builtins.property
    def name(self) -> builtins.str:
        """``AWS::DataBrew::Job.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-job.html#cfn-databrew-job-name
        """
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return result

    @builtins.property
    def role_arn(self) -> builtins.str:
        """``AWS::DataBrew::Job.RoleArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-job.html#cfn-databrew-job-rolearn
        """
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return result

    @builtins.property
    def type(self) -> builtins.str:
        """``AWS::DataBrew::Job.Type``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-job.html#cfn-databrew-job-type
        """
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return result

    @builtins.property
    def dataset_name(self) -> typing.Optional[builtins.str]:
        """``AWS::DataBrew::Job.DatasetName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-job.html#cfn-databrew-job-datasetname
        """
        result = self._values.get("dataset_name")
        return result

    @builtins.property
    def encryption_key_arn(self) -> typing.Optional[builtins.str]:
        """``AWS::DataBrew::Job.EncryptionKeyArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-job.html#cfn-databrew-job-encryptionkeyarn
        """
        result = self._values.get("encryption_key_arn")
        return result

    @builtins.property
    def encryption_mode(self) -> typing.Optional[builtins.str]:
        """``AWS::DataBrew::Job.EncryptionMode``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-job.html#cfn-databrew-job-encryptionmode
        """
        result = self._values.get("encryption_mode")
        return result

    @builtins.property
    def log_subscription(self) -> typing.Optional[builtins.str]:
        """``AWS::DataBrew::Job.LogSubscription``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-job.html#cfn-databrew-job-logsubscription
        """
        result = self._values.get("log_subscription")
        return result

    @builtins.property
    def max_capacity(self) -> typing.Optional[jsii.Number]:
        """``AWS::DataBrew::Job.MaxCapacity``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-job.html#cfn-databrew-job-maxcapacity
        """
        result = self._values.get("max_capacity")
        return result

    @builtins.property
    def max_retries(self) -> typing.Optional[jsii.Number]:
        """``AWS::DataBrew::Job.MaxRetries``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-job.html#cfn-databrew-job-maxretries
        """
        result = self._values.get("max_retries")
        return result

    @builtins.property
    def output_location(self) -> typing.Any:
        """``AWS::DataBrew::Job.OutputLocation``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-job.html#cfn-databrew-job-outputlocation
        """
        result = self._values.get("output_location")
        return result

    @builtins.property
    def outputs(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnJob.OutputProperty]]]]:
        """``AWS::DataBrew::Job.Outputs``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-job.html#cfn-databrew-job-outputs
        """
        result = self._values.get("outputs")
        return result

    @builtins.property
    def project_name(self) -> typing.Optional[builtins.str]:
        """``AWS::DataBrew::Job.ProjectName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-job.html#cfn-databrew-job-projectname
        """
        result = self._values.get("project_name")
        return result

    @builtins.property
    def recipe(self) -> typing.Any:
        """``AWS::DataBrew::Job.Recipe``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-job.html#cfn-databrew-job-recipe
        """
        result = self._values.get("recipe")
        return result

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        """``AWS::DataBrew::Job.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-job.html#cfn-databrew-job-tags
        """
        result = self._values.get("tags")
        return result

    @builtins.property
    def timeout(self) -> typing.Optional[jsii.Number]:
        """``AWS::DataBrew::Job.Timeout``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-job.html#cfn-databrew-job-timeout
        """
        result = self._values.get("timeout")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnJobProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnProject(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-databrew.CfnProject",
):
    """A CloudFormation ``AWS::DataBrew::Project``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-project.html
    :cloudformationResource: AWS::DataBrew::Project
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        dataset_name: builtins.str,
        name: builtins.str,
        recipe_name: builtins.str,
        role_arn: builtins.str,
        sample: typing.Any = None,
        tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]] = None,
    ) -> None:
        """Create a new ``AWS::DataBrew::Project``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param dataset_name: ``AWS::DataBrew::Project.DatasetName``.
        :param name: ``AWS::DataBrew::Project.Name``.
        :param recipe_name: ``AWS::DataBrew::Project.RecipeName``.
        :param role_arn: ``AWS::DataBrew::Project.RoleArn``.
        :param sample: ``AWS::DataBrew::Project.Sample``.
        :param tags: ``AWS::DataBrew::Project.Tags``.
        """
        props = CfnProjectProps(
            dataset_name=dataset_name,
            name=name,
            recipe_name=recipe_name,
            role_arn=role_arn,
            sample=sample,
            tags=tags,
        )

        jsii.create(CfnProject, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        """(experimental) Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        """``AWS::DataBrew::Project.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-project.html#cfn-databrew-project-tags
        """
        return jsii.get(self, "tags")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="datasetName")
    def dataset_name(self) -> builtins.str:
        """``AWS::DataBrew::Project.DatasetName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-project.html#cfn-databrew-project-datasetname
        """
        return jsii.get(self, "datasetName")

    @dataset_name.setter # type: ignore
    def dataset_name(self, value: builtins.str) -> None:
        jsii.set(self, "datasetName", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        """``AWS::DataBrew::Project.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-project.html#cfn-databrew-project-name
        """
        return jsii.get(self, "name")

    @name.setter # type: ignore
    def name(self, value: builtins.str) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="recipeName")
    def recipe_name(self) -> builtins.str:
        """``AWS::DataBrew::Project.RecipeName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-project.html#cfn-databrew-project-recipename
        """
        return jsii.get(self, "recipeName")

    @recipe_name.setter # type: ignore
    def recipe_name(self, value: builtins.str) -> None:
        jsii.set(self, "recipeName", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        """``AWS::DataBrew::Project.RoleArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-project.html#cfn-databrew-project-rolearn
        """
        return jsii.get(self, "roleArn")

    @role_arn.setter # type: ignore
    def role_arn(self, value: builtins.str) -> None:
        jsii.set(self, "roleArn", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="sample")
    def sample(self) -> typing.Any:
        """``AWS::DataBrew::Project.Sample``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-project.html#cfn-databrew-project-sample
        """
        return jsii.get(self, "sample")

    @sample.setter # type: ignore
    def sample(self, value: typing.Any) -> None:
        jsii.set(self, "sample", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-databrew.CfnProjectProps",
    jsii_struct_bases=[],
    name_mapping={
        "dataset_name": "datasetName",
        "name": "name",
        "recipe_name": "recipeName",
        "role_arn": "roleArn",
        "sample": "sample",
        "tags": "tags",
    },
)
class CfnProjectProps:
    def __init__(
        self,
        *,
        dataset_name: builtins.str,
        name: builtins.str,
        recipe_name: builtins.str,
        role_arn: builtins.str,
        sample: typing.Any = None,
        tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]] = None,
    ) -> None:
        """Properties for defining a ``AWS::DataBrew::Project``.

        :param dataset_name: ``AWS::DataBrew::Project.DatasetName``.
        :param name: ``AWS::DataBrew::Project.Name``.
        :param recipe_name: ``AWS::DataBrew::Project.RecipeName``.
        :param role_arn: ``AWS::DataBrew::Project.RoleArn``.
        :param sample: ``AWS::DataBrew::Project.Sample``.
        :param tags: ``AWS::DataBrew::Project.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-project.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "dataset_name": dataset_name,
            "name": name,
            "recipe_name": recipe_name,
            "role_arn": role_arn,
        }
        if sample is not None:
            self._values["sample"] = sample
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def dataset_name(self) -> builtins.str:
        """``AWS::DataBrew::Project.DatasetName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-project.html#cfn-databrew-project-datasetname
        """
        result = self._values.get("dataset_name")
        assert result is not None, "Required property 'dataset_name' is missing"
        return result

    @builtins.property
    def name(self) -> builtins.str:
        """``AWS::DataBrew::Project.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-project.html#cfn-databrew-project-name
        """
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return result

    @builtins.property
    def recipe_name(self) -> builtins.str:
        """``AWS::DataBrew::Project.RecipeName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-project.html#cfn-databrew-project-recipename
        """
        result = self._values.get("recipe_name")
        assert result is not None, "Required property 'recipe_name' is missing"
        return result

    @builtins.property
    def role_arn(self) -> builtins.str:
        """``AWS::DataBrew::Project.RoleArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-project.html#cfn-databrew-project-rolearn
        """
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return result

    @builtins.property
    def sample(self) -> typing.Any:
        """``AWS::DataBrew::Project.Sample``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-project.html#cfn-databrew-project-sample
        """
        result = self._values.get("sample")
        return result

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        """``AWS::DataBrew::Project.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-project.html#cfn-databrew-project-tags
        """
        result = self._values.get("tags")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnProjectProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnRecipe(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-databrew.CfnRecipe",
):
    """A CloudFormation ``AWS::DataBrew::Recipe``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-recipe.html
    :cloudformationResource: AWS::DataBrew::Recipe
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        steps: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnRecipe.RecipeStepProperty"]]],
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]] = None,
    ) -> None:
        """Create a new ``AWS::DataBrew::Recipe``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: ``AWS::DataBrew::Recipe.Name``.
        :param steps: ``AWS::DataBrew::Recipe.Steps``.
        :param description: ``AWS::DataBrew::Recipe.Description``.
        :param tags: ``AWS::DataBrew::Recipe.Tags``.
        """
        props = CfnRecipeProps(
            name=name, steps=steps, description=description, tags=tags
        )

        jsii.create(CfnRecipe, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        """(experimental) Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        """``AWS::DataBrew::Recipe.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-recipe.html#cfn-databrew-recipe-tags
        """
        return jsii.get(self, "tags")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        """``AWS::DataBrew::Recipe.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-recipe.html#cfn-databrew-recipe-name
        """
        return jsii.get(self, "name")

    @name.setter # type: ignore
    def name(self, value: builtins.str) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="steps")
    def steps(
        self,
    ) -> typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnRecipe.RecipeStepProperty"]]]:
        """``AWS::DataBrew::Recipe.Steps``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-recipe.html#cfn-databrew-recipe-steps
        """
        return jsii.get(self, "steps")

    @steps.setter # type: ignore
    def steps(
        self,
        value: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnRecipe.RecipeStepProperty"]]],
    ) -> None:
        jsii.set(self, "steps", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        """``AWS::DataBrew::Recipe.Description``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-recipe.html#cfn-databrew-recipe-description
        """
        return jsii.get(self, "description")

    @description.setter # type: ignore
    def description(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "description", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-databrew.CfnRecipe.ActionProperty",
        jsii_struct_bases=[],
        name_mapping={"operation": "operation", "parameters": "parameters"},
    )
    class ActionProperty:
        def __init__(
            self,
            *,
            operation: builtins.str,
            parameters: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Mapping[builtins.str, builtins.str]]] = None,
        ) -> None:
            """
            :param operation: ``CfnRecipe.ActionProperty.Operation``.
            :param parameters: ``CfnRecipe.ActionProperty.Parameters``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-action.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "operation": operation,
            }
            if parameters is not None:
                self._values["parameters"] = parameters

        @builtins.property
        def operation(self) -> builtins.str:
            """``CfnRecipe.ActionProperty.Operation``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-action.html#cfn-databrew-recipe-action-operation
            """
            result = self._values.get("operation")
            assert result is not None, "Required property 'operation' is missing"
            return result

        @builtins.property
        def parameters(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Mapping[builtins.str, builtins.str]]]:
            """``CfnRecipe.ActionProperty.Parameters``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-action.html#cfn-databrew-recipe-action-parameters
            """
            result = self._values.get("parameters")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-databrew.CfnRecipe.ConditionExpressionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "condition": "condition",
            "target_column": "targetColumn",
            "value": "value",
        },
    )
    class ConditionExpressionProperty:
        def __init__(
            self,
            *,
            condition: builtins.str,
            target_column: builtins.str,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param condition: ``CfnRecipe.ConditionExpressionProperty.Condition``.
            :param target_column: ``CfnRecipe.ConditionExpressionProperty.TargetColumn``.
            :param value: ``CfnRecipe.ConditionExpressionProperty.Value``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-conditionexpression.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "condition": condition,
                "target_column": target_column,
            }
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def condition(self) -> builtins.str:
            """``CfnRecipe.ConditionExpressionProperty.Condition``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-conditionexpression.html#cfn-databrew-recipe-conditionexpression-condition
            """
            result = self._values.get("condition")
            assert result is not None, "Required property 'condition' is missing"
            return result

        @builtins.property
        def target_column(self) -> builtins.str:
            """``CfnRecipe.ConditionExpressionProperty.TargetColumn``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-conditionexpression.html#cfn-databrew-recipe-conditionexpression-targetcolumn
            """
            result = self._values.get("target_column")
            assert result is not None, "Required property 'target_column' is missing"
            return result

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            """``CfnRecipe.ConditionExpressionProperty.Value``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-conditionexpression.html#cfn-databrew-recipe-conditionexpression-value
            """
            result = self._values.get("value")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConditionExpressionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-databrew.CfnRecipe.DataCatalogInputDefinitionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "catalog_id": "catalogId",
            "database_name": "databaseName",
            "table_name": "tableName",
            "temp_directory": "tempDirectory",
        },
    )
    class DataCatalogInputDefinitionProperty:
        def __init__(
            self,
            *,
            catalog_id: typing.Optional[builtins.str] = None,
            database_name: typing.Optional[builtins.str] = None,
            table_name: typing.Optional[builtins.str] = None,
            temp_directory: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRecipe.S3LocationProperty"]] = None,
        ) -> None:
            """
            :param catalog_id: ``CfnRecipe.DataCatalogInputDefinitionProperty.CatalogId``.
            :param database_name: ``CfnRecipe.DataCatalogInputDefinitionProperty.DatabaseName``.
            :param table_name: ``CfnRecipe.DataCatalogInputDefinitionProperty.TableName``.
            :param temp_directory: ``CfnRecipe.DataCatalogInputDefinitionProperty.TempDirectory``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-datacataloginputdefinition.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if catalog_id is not None:
                self._values["catalog_id"] = catalog_id
            if database_name is not None:
                self._values["database_name"] = database_name
            if table_name is not None:
                self._values["table_name"] = table_name
            if temp_directory is not None:
                self._values["temp_directory"] = temp_directory

        @builtins.property
        def catalog_id(self) -> typing.Optional[builtins.str]:
            """``CfnRecipe.DataCatalogInputDefinitionProperty.CatalogId``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-datacataloginputdefinition.html#cfn-databrew-recipe-datacataloginputdefinition-catalogid
            """
            result = self._values.get("catalog_id")
            return result

        @builtins.property
        def database_name(self) -> typing.Optional[builtins.str]:
            """``CfnRecipe.DataCatalogInputDefinitionProperty.DatabaseName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-datacataloginputdefinition.html#cfn-databrew-recipe-datacataloginputdefinition-databasename
            """
            result = self._values.get("database_name")
            return result

        @builtins.property
        def table_name(self) -> typing.Optional[builtins.str]:
            """``CfnRecipe.DataCatalogInputDefinitionProperty.TableName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-datacataloginputdefinition.html#cfn-databrew-recipe-datacataloginputdefinition-tablename
            """
            result = self._values.get("table_name")
            return result

        @builtins.property
        def temp_directory(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRecipe.S3LocationProperty"]]:
            """``CfnRecipe.DataCatalogInputDefinitionProperty.TempDirectory``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-datacataloginputdefinition.html#cfn-databrew-recipe-datacataloginputdefinition-tempdirectory
            """
            result = self._values.get("temp_directory")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DataCatalogInputDefinitionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-databrew.CfnRecipe.RecipeParametersProperty",
        jsii_struct_bases=[],
        name_mapping={
            "aggregate_function": "aggregateFunction",
            "base": "base",
            "case_statement": "caseStatement",
            "category_map": "categoryMap",
            "chars_to_remove": "charsToRemove",
            "collapse_consecutive_whitespace": "collapseConsecutiveWhitespace",
            "column_data_type": "columnDataType",
            "column_range": "columnRange",
            "count": "count",
            "custom_characters": "customCharacters",
            "custom_stop_words": "customStopWords",
            "custom_value": "customValue",
            "datasets_columns": "datasetsColumns",
            "date_add_value": "dateAddValue",
            "date_time_format": "dateTimeFormat",
            "date_time_parameters": "dateTimeParameters",
            "delete_other_rows": "deleteOtherRows",
            "delimiter": "delimiter",
            "end_pattern": "endPattern",
            "end_position": "endPosition",
            "end_value": "endValue",
            "expand_contractions": "expandContractions",
            "exponent": "exponent",
            "false_string": "falseString",
            "group_by_agg_function_options": "groupByAggFunctionOptions",
            "group_by_columns": "groupByColumns",
            "hidden_columns": "hiddenColumns",
            "ignore_case": "ignoreCase",
            "include_in_split": "includeInSplit",
            "input": "input",
            "interval": "interval",
            "is_text": "isText",
            "join_keys": "joinKeys",
            "join_type": "joinType",
            "left_columns": "leftColumns",
            "limit": "limit",
            "lower_bound": "lowerBound",
            "map_type": "mapType",
            "mode_type": "modeType",
            "multi_line": "multiLine",
            "num_rows": "numRows",
            "num_rows_after": "numRowsAfter",
            "num_rows_before": "numRowsBefore",
            "order_by_column": "orderByColumn",
            "order_by_columns": "orderByColumns",
            "other": "other",
            "pattern": "pattern",
            "pattern_option1": "patternOption1",
            "pattern_option2": "patternOption2",
            "pattern_options": "patternOptions",
            "period": "period",
            "position": "position",
            "remove_all_punctuation": "removeAllPunctuation",
            "remove_all_quotes": "removeAllQuotes",
            "remove_all_whitespace": "removeAllWhitespace",
            "remove_custom_characters": "removeCustomCharacters",
            "remove_custom_value": "removeCustomValue",
            "remove_leading_and_trailing_punctuation": "removeLeadingAndTrailingPunctuation",
            "remove_leading_and_trailing_quotes": "removeLeadingAndTrailingQuotes",
            "remove_leading_and_trailing_whitespace": "removeLeadingAndTrailingWhitespace",
            "remove_letters": "removeLetters",
            "remove_numbers": "removeNumbers",
            "remove_source_column": "removeSourceColumn",
            "remove_special_characters": "removeSpecialCharacters",
            "right_columns": "rightColumns",
            "sample_size": "sampleSize",
            "sample_type": "sampleType",
            "secondary_inputs": "secondaryInputs",
            "second_input": "secondInput",
            "sheet_indexes": "sheetIndexes",
            "sheet_names": "sheetNames",
            "source_column": "sourceColumn",
            "source_column1": "sourceColumn1",
            "source_column2": "sourceColumn2",
            "source_columns": "sourceColumns",
            "start_column_index": "startColumnIndex",
            "start_pattern": "startPattern",
            "start_position": "startPosition",
            "start_value": "startValue",
            "stemming_mode": "stemmingMode",
            "step_count": "stepCount",
            "step_index": "stepIndex",
            "stop_words_mode": "stopWordsMode",
            "strategy": "strategy",
            "target_column": "targetColumn",
            "target_column_names": "targetColumnNames",
            "target_date_format": "targetDateFormat",
            "target_index": "targetIndex",
            "time_zone": "timeZone",
            "tokenizer_pattern": "tokenizerPattern",
            "true_string": "trueString",
            "udf_lang": "udfLang",
            "units": "units",
            "unpivot_column": "unpivotColumn",
            "upper_bound": "upperBound",
            "use_new_data_frame": "useNewDataFrame",
            "value": "value",
            "value1": "value1",
            "value2": "value2",
            "value_column": "valueColumn",
            "view_frame": "viewFrame",
        },
    )
    class RecipeParametersProperty:
        def __init__(
            self,
            *,
            aggregate_function: typing.Optional[builtins.str] = None,
            base: typing.Optional[builtins.str] = None,
            case_statement: typing.Optional[builtins.str] = None,
            category_map: typing.Optional[builtins.str] = None,
            chars_to_remove: typing.Optional[builtins.str] = None,
            collapse_consecutive_whitespace: typing.Optional[builtins.str] = None,
            column_data_type: typing.Optional[builtins.str] = None,
            column_range: typing.Optional[builtins.str] = None,
            count: typing.Optional[builtins.str] = None,
            custom_characters: typing.Optional[builtins.str] = None,
            custom_stop_words: typing.Optional[builtins.str] = None,
            custom_value: typing.Optional[builtins.str] = None,
            datasets_columns: typing.Optional[builtins.str] = None,
            date_add_value: typing.Optional[builtins.str] = None,
            date_time_format: typing.Optional[builtins.str] = None,
            date_time_parameters: typing.Optional[builtins.str] = None,
            delete_other_rows: typing.Optional[builtins.str] = None,
            delimiter: typing.Optional[builtins.str] = None,
            end_pattern: typing.Optional[builtins.str] = None,
            end_position: typing.Optional[builtins.str] = None,
            end_value: typing.Optional[builtins.str] = None,
            expand_contractions: typing.Optional[builtins.str] = None,
            exponent: typing.Optional[builtins.str] = None,
            false_string: typing.Optional[builtins.str] = None,
            group_by_agg_function_options: typing.Optional[builtins.str] = None,
            group_by_columns: typing.Optional[builtins.str] = None,
            hidden_columns: typing.Optional[builtins.str] = None,
            ignore_case: typing.Optional[builtins.str] = None,
            include_in_split: typing.Optional[builtins.str] = None,
            input: typing.Any = None,
            interval: typing.Optional[builtins.str] = None,
            is_text: typing.Optional[builtins.str] = None,
            join_keys: typing.Optional[builtins.str] = None,
            join_type: typing.Optional[builtins.str] = None,
            left_columns: typing.Optional[builtins.str] = None,
            limit: typing.Optional[builtins.str] = None,
            lower_bound: typing.Optional[builtins.str] = None,
            map_type: typing.Optional[builtins.str] = None,
            mode_type: typing.Optional[builtins.str] = None,
            multi_line: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
            num_rows: typing.Optional[builtins.str] = None,
            num_rows_after: typing.Optional[builtins.str] = None,
            num_rows_before: typing.Optional[builtins.str] = None,
            order_by_column: typing.Optional[builtins.str] = None,
            order_by_columns: typing.Optional[builtins.str] = None,
            other: typing.Optional[builtins.str] = None,
            pattern: typing.Optional[builtins.str] = None,
            pattern_option1: typing.Optional[builtins.str] = None,
            pattern_option2: typing.Optional[builtins.str] = None,
            pattern_options: typing.Optional[builtins.str] = None,
            period: typing.Optional[builtins.str] = None,
            position: typing.Optional[builtins.str] = None,
            remove_all_punctuation: typing.Optional[builtins.str] = None,
            remove_all_quotes: typing.Optional[builtins.str] = None,
            remove_all_whitespace: typing.Optional[builtins.str] = None,
            remove_custom_characters: typing.Optional[builtins.str] = None,
            remove_custom_value: typing.Optional[builtins.str] = None,
            remove_leading_and_trailing_punctuation: typing.Optional[builtins.str] = None,
            remove_leading_and_trailing_quotes: typing.Optional[builtins.str] = None,
            remove_leading_and_trailing_whitespace: typing.Optional[builtins.str] = None,
            remove_letters: typing.Optional[builtins.str] = None,
            remove_numbers: typing.Optional[builtins.str] = None,
            remove_source_column: typing.Optional[builtins.str] = None,
            remove_special_characters: typing.Optional[builtins.str] = None,
            right_columns: typing.Optional[builtins.str] = None,
            sample_size: typing.Optional[builtins.str] = None,
            sample_type: typing.Optional[builtins.str] = None,
            secondary_inputs: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnRecipe.SecondaryInputProperty"]]]] = None,
            second_input: typing.Optional[builtins.str] = None,
            sheet_indexes: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[jsii.Number]]] = None,
            sheet_names: typing.Optional[typing.List[builtins.str]] = None,
            source_column: typing.Optional[builtins.str] = None,
            source_column1: typing.Optional[builtins.str] = None,
            source_column2: typing.Optional[builtins.str] = None,
            source_columns: typing.Optional[builtins.str] = None,
            start_column_index: typing.Optional[builtins.str] = None,
            start_pattern: typing.Optional[builtins.str] = None,
            start_position: typing.Optional[builtins.str] = None,
            start_value: typing.Optional[builtins.str] = None,
            stemming_mode: typing.Optional[builtins.str] = None,
            step_count: typing.Optional[builtins.str] = None,
            step_index: typing.Optional[builtins.str] = None,
            stop_words_mode: typing.Optional[builtins.str] = None,
            strategy: typing.Optional[builtins.str] = None,
            target_column: typing.Optional[builtins.str] = None,
            target_column_names: typing.Optional[builtins.str] = None,
            target_date_format: typing.Optional[builtins.str] = None,
            target_index: typing.Optional[builtins.str] = None,
            time_zone: typing.Optional[builtins.str] = None,
            tokenizer_pattern: typing.Optional[builtins.str] = None,
            true_string: typing.Optional[builtins.str] = None,
            udf_lang: typing.Optional[builtins.str] = None,
            units: typing.Optional[builtins.str] = None,
            unpivot_column: typing.Optional[builtins.str] = None,
            upper_bound: typing.Optional[builtins.str] = None,
            use_new_data_frame: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
            value1: typing.Optional[builtins.str] = None,
            value2: typing.Optional[builtins.str] = None,
            value_column: typing.Optional[builtins.str] = None,
            view_frame: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param aggregate_function: ``CfnRecipe.RecipeParametersProperty.AggregateFunction``.
            :param base: ``CfnRecipe.RecipeParametersProperty.Base``.
            :param case_statement: ``CfnRecipe.RecipeParametersProperty.CaseStatement``.
            :param category_map: ``CfnRecipe.RecipeParametersProperty.CategoryMap``.
            :param chars_to_remove: ``CfnRecipe.RecipeParametersProperty.CharsToRemove``.
            :param collapse_consecutive_whitespace: ``CfnRecipe.RecipeParametersProperty.CollapseConsecutiveWhitespace``.
            :param column_data_type: ``CfnRecipe.RecipeParametersProperty.ColumnDataType``.
            :param column_range: ``CfnRecipe.RecipeParametersProperty.ColumnRange``.
            :param count: ``CfnRecipe.RecipeParametersProperty.Count``.
            :param custom_characters: ``CfnRecipe.RecipeParametersProperty.CustomCharacters``.
            :param custom_stop_words: ``CfnRecipe.RecipeParametersProperty.CustomStopWords``.
            :param custom_value: ``CfnRecipe.RecipeParametersProperty.CustomValue``.
            :param datasets_columns: ``CfnRecipe.RecipeParametersProperty.DatasetsColumns``.
            :param date_add_value: ``CfnRecipe.RecipeParametersProperty.DateAddValue``.
            :param date_time_format: ``CfnRecipe.RecipeParametersProperty.DateTimeFormat``.
            :param date_time_parameters: ``CfnRecipe.RecipeParametersProperty.DateTimeParameters``.
            :param delete_other_rows: ``CfnRecipe.RecipeParametersProperty.DeleteOtherRows``.
            :param delimiter: ``CfnRecipe.RecipeParametersProperty.Delimiter``.
            :param end_pattern: ``CfnRecipe.RecipeParametersProperty.EndPattern``.
            :param end_position: ``CfnRecipe.RecipeParametersProperty.EndPosition``.
            :param end_value: ``CfnRecipe.RecipeParametersProperty.EndValue``.
            :param expand_contractions: ``CfnRecipe.RecipeParametersProperty.ExpandContractions``.
            :param exponent: ``CfnRecipe.RecipeParametersProperty.Exponent``.
            :param false_string: ``CfnRecipe.RecipeParametersProperty.FalseString``.
            :param group_by_agg_function_options: ``CfnRecipe.RecipeParametersProperty.GroupByAggFunctionOptions``.
            :param group_by_columns: ``CfnRecipe.RecipeParametersProperty.GroupByColumns``.
            :param hidden_columns: ``CfnRecipe.RecipeParametersProperty.HiddenColumns``.
            :param ignore_case: ``CfnRecipe.RecipeParametersProperty.IgnoreCase``.
            :param include_in_split: ``CfnRecipe.RecipeParametersProperty.IncludeInSplit``.
            :param input: ``CfnRecipe.RecipeParametersProperty.Input``.
            :param interval: ``CfnRecipe.RecipeParametersProperty.Interval``.
            :param is_text: ``CfnRecipe.RecipeParametersProperty.IsText``.
            :param join_keys: ``CfnRecipe.RecipeParametersProperty.JoinKeys``.
            :param join_type: ``CfnRecipe.RecipeParametersProperty.JoinType``.
            :param left_columns: ``CfnRecipe.RecipeParametersProperty.LeftColumns``.
            :param limit: ``CfnRecipe.RecipeParametersProperty.Limit``.
            :param lower_bound: ``CfnRecipe.RecipeParametersProperty.LowerBound``.
            :param map_type: ``CfnRecipe.RecipeParametersProperty.MapType``.
            :param mode_type: ``CfnRecipe.RecipeParametersProperty.ModeType``.
            :param multi_line: ``CfnRecipe.RecipeParametersProperty.MultiLine``.
            :param num_rows: ``CfnRecipe.RecipeParametersProperty.NumRows``.
            :param num_rows_after: ``CfnRecipe.RecipeParametersProperty.NumRowsAfter``.
            :param num_rows_before: ``CfnRecipe.RecipeParametersProperty.NumRowsBefore``.
            :param order_by_column: ``CfnRecipe.RecipeParametersProperty.OrderByColumn``.
            :param order_by_columns: ``CfnRecipe.RecipeParametersProperty.OrderByColumns``.
            :param other: ``CfnRecipe.RecipeParametersProperty.Other``.
            :param pattern: ``CfnRecipe.RecipeParametersProperty.Pattern``.
            :param pattern_option1: ``CfnRecipe.RecipeParametersProperty.PatternOption1``.
            :param pattern_option2: ``CfnRecipe.RecipeParametersProperty.PatternOption2``.
            :param pattern_options: ``CfnRecipe.RecipeParametersProperty.PatternOptions``.
            :param period: ``CfnRecipe.RecipeParametersProperty.Period``.
            :param position: ``CfnRecipe.RecipeParametersProperty.Position``.
            :param remove_all_punctuation: ``CfnRecipe.RecipeParametersProperty.RemoveAllPunctuation``.
            :param remove_all_quotes: ``CfnRecipe.RecipeParametersProperty.RemoveAllQuotes``.
            :param remove_all_whitespace: ``CfnRecipe.RecipeParametersProperty.RemoveAllWhitespace``.
            :param remove_custom_characters: ``CfnRecipe.RecipeParametersProperty.RemoveCustomCharacters``.
            :param remove_custom_value: ``CfnRecipe.RecipeParametersProperty.RemoveCustomValue``.
            :param remove_leading_and_trailing_punctuation: ``CfnRecipe.RecipeParametersProperty.RemoveLeadingAndTrailingPunctuation``.
            :param remove_leading_and_trailing_quotes: ``CfnRecipe.RecipeParametersProperty.RemoveLeadingAndTrailingQuotes``.
            :param remove_leading_and_trailing_whitespace: ``CfnRecipe.RecipeParametersProperty.RemoveLeadingAndTrailingWhitespace``.
            :param remove_letters: ``CfnRecipe.RecipeParametersProperty.RemoveLetters``.
            :param remove_numbers: ``CfnRecipe.RecipeParametersProperty.RemoveNumbers``.
            :param remove_source_column: ``CfnRecipe.RecipeParametersProperty.RemoveSourceColumn``.
            :param remove_special_characters: ``CfnRecipe.RecipeParametersProperty.RemoveSpecialCharacters``.
            :param right_columns: ``CfnRecipe.RecipeParametersProperty.RightColumns``.
            :param sample_size: ``CfnRecipe.RecipeParametersProperty.SampleSize``.
            :param sample_type: ``CfnRecipe.RecipeParametersProperty.SampleType``.
            :param secondary_inputs: ``CfnRecipe.RecipeParametersProperty.SecondaryInputs``.
            :param second_input: ``CfnRecipe.RecipeParametersProperty.SecondInput``.
            :param sheet_indexes: ``CfnRecipe.RecipeParametersProperty.SheetIndexes``.
            :param sheet_names: ``CfnRecipe.RecipeParametersProperty.SheetNames``.
            :param source_column: ``CfnRecipe.RecipeParametersProperty.SourceColumn``.
            :param source_column1: ``CfnRecipe.RecipeParametersProperty.SourceColumn1``.
            :param source_column2: ``CfnRecipe.RecipeParametersProperty.SourceColumn2``.
            :param source_columns: ``CfnRecipe.RecipeParametersProperty.SourceColumns``.
            :param start_column_index: ``CfnRecipe.RecipeParametersProperty.StartColumnIndex``.
            :param start_pattern: ``CfnRecipe.RecipeParametersProperty.StartPattern``.
            :param start_position: ``CfnRecipe.RecipeParametersProperty.StartPosition``.
            :param start_value: ``CfnRecipe.RecipeParametersProperty.StartValue``.
            :param stemming_mode: ``CfnRecipe.RecipeParametersProperty.StemmingMode``.
            :param step_count: ``CfnRecipe.RecipeParametersProperty.StepCount``.
            :param step_index: ``CfnRecipe.RecipeParametersProperty.StepIndex``.
            :param stop_words_mode: ``CfnRecipe.RecipeParametersProperty.StopWordsMode``.
            :param strategy: ``CfnRecipe.RecipeParametersProperty.Strategy``.
            :param target_column: ``CfnRecipe.RecipeParametersProperty.TargetColumn``.
            :param target_column_names: ``CfnRecipe.RecipeParametersProperty.TargetColumnNames``.
            :param target_date_format: ``CfnRecipe.RecipeParametersProperty.TargetDateFormat``.
            :param target_index: ``CfnRecipe.RecipeParametersProperty.TargetIndex``.
            :param time_zone: ``CfnRecipe.RecipeParametersProperty.TimeZone``.
            :param tokenizer_pattern: ``CfnRecipe.RecipeParametersProperty.TokenizerPattern``.
            :param true_string: ``CfnRecipe.RecipeParametersProperty.TrueString``.
            :param udf_lang: ``CfnRecipe.RecipeParametersProperty.UdfLang``.
            :param units: ``CfnRecipe.RecipeParametersProperty.Units``.
            :param unpivot_column: ``CfnRecipe.RecipeParametersProperty.UnpivotColumn``.
            :param upper_bound: ``CfnRecipe.RecipeParametersProperty.UpperBound``.
            :param use_new_data_frame: ``CfnRecipe.RecipeParametersProperty.UseNewDataFrame``.
            :param value: ``CfnRecipe.RecipeParametersProperty.Value``.
            :param value1: ``CfnRecipe.RecipeParametersProperty.Value1``.
            :param value2: ``CfnRecipe.RecipeParametersProperty.Value2``.
            :param value_column: ``CfnRecipe.RecipeParametersProperty.ValueColumn``.
            :param view_frame: ``CfnRecipe.RecipeParametersProperty.ViewFrame``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipeparameters.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if aggregate_function is not None:
                self._values["aggregate_function"] = aggregate_function
            if base is not None:
                self._values["base"] = base
            if case_statement is not None:
                self._values["case_statement"] = case_statement
            if category_map is not None:
                self._values["category_map"] = category_map
            if chars_to_remove is not None:
                self._values["chars_to_remove"] = chars_to_remove
            if collapse_consecutive_whitespace is not None:
                self._values["collapse_consecutive_whitespace"] = collapse_consecutive_whitespace
            if column_data_type is not None:
                self._values["column_data_type"] = column_data_type
            if column_range is not None:
                self._values["column_range"] = column_range
            if count is not None:
                self._values["count"] = count
            if custom_characters is not None:
                self._values["custom_characters"] = custom_characters
            if custom_stop_words is not None:
                self._values["custom_stop_words"] = custom_stop_words
            if custom_value is not None:
                self._values["custom_value"] = custom_value
            if datasets_columns is not None:
                self._values["datasets_columns"] = datasets_columns
            if date_add_value is not None:
                self._values["date_add_value"] = date_add_value
            if date_time_format is not None:
                self._values["date_time_format"] = date_time_format
            if date_time_parameters is not None:
                self._values["date_time_parameters"] = date_time_parameters
            if delete_other_rows is not None:
                self._values["delete_other_rows"] = delete_other_rows
            if delimiter is not None:
                self._values["delimiter"] = delimiter
            if end_pattern is not None:
                self._values["end_pattern"] = end_pattern
            if end_position is not None:
                self._values["end_position"] = end_position
            if end_value is not None:
                self._values["end_value"] = end_value
            if expand_contractions is not None:
                self._values["expand_contractions"] = expand_contractions
            if exponent is not None:
                self._values["exponent"] = exponent
            if false_string is not None:
                self._values["false_string"] = false_string
            if group_by_agg_function_options is not None:
                self._values["group_by_agg_function_options"] = group_by_agg_function_options
            if group_by_columns is not None:
                self._values["group_by_columns"] = group_by_columns
            if hidden_columns is not None:
                self._values["hidden_columns"] = hidden_columns
            if ignore_case is not None:
                self._values["ignore_case"] = ignore_case
            if include_in_split is not None:
                self._values["include_in_split"] = include_in_split
            if input is not None:
                self._values["input"] = input
            if interval is not None:
                self._values["interval"] = interval
            if is_text is not None:
                self._values["is_text"] = is_text
            if join_keys is not None:
                self._values["join_keys"] = join_keys
            if join_type is not None:
                self._values["join_type"] = join_type
            if left_columns is not None:
                self._values["left_columns"] = left_columns
            if limit is not None:
                self._values["limit"] = limit
            if lower_bound is not None:
                self._values["lower_bound"] = lower_bound
            if map_type is not None:
                self._values["map_type"] = map_type
            if mode_type is not None:
                self._values["mode_type"] = mode_type
            if multi_line is not None:
                self._values["multi_line"] = multi_line
            if num_rows is not None:
                self._values["num_rows"] = num_rows
            if num_rows_after is not None:
                self._values["num_rows_after"] = num_rows_after
            if num_rows_before is not None:
                self._values["num_rows_before"] = num_rows_before
            if order_by_column is not None:
                self._values["order_by_column"] = order_by_column
            if order_by_columns is not None:
                self._values["order_by_columns"] = order_by_columns
            if other is not None:
                self._values["other"] = other
            if pattern is not None:
                self._values["pattern"] = pattern
            if pattern_option1 is not None:
                self._values["pattern_option1"] = pattern_option1
            if pattern_option2 is not None:
                self._values["pattern_option2"] = pattern_option2
            if pattern_options is not None:
                self._values["pattern_options"] = pattern_options
            if period is not None:
                self._values["period"] = period
            if position is not None:
                self._values["position"] = position
            if remove_all_punctuation is not None:
                self._values["remove_all_punctuation"] = remove_all_punctuation
            if remove_all_quotes is not None:
                self._values["remove_all_quotes"] = remove_all_quotes
            if remove_all_whitespace is not None:
                self._values["remove_all_whitespace"] = remove_all_whitespace
            if remove_custom_characters is not None:
                self._values["remove_custom_characters"] = remove_custom_characters
            if remove_custom_value is not None:
                self._values["remove_custom_value"] = remove_custom_value
            if remove_leading_and_trailing_punctuation is not None:
                self._values["remove_leading_and_trailing_punctuation"] = remove_leading_and_trailing_punctuation
            if remove_leading_and_trailing_quotes is not None:
                self._values["remove_leading_and_trailing_quotes"] = remove_leading_and_trailing_quotes
            if remove_leading_and_trailing_whitespace is not None:
                self._values["remove_leading_and_trailing_whitespace"] = remove_leading_and_trailing_whitespace
            if remove_letters is not None:
                self._values["remove_letters"] = remove_letters
            if remove_numbers is not None:
                self._values["remove_numbers"] = remove_numbers
            if remove_source_column is not None:
                self._values["remove_source_column"] = remove_source_column
            if remove_special_characters is not None:
                self._values["remove_special_characters"] = remove_special_characters
            if right_columns is not None:
                self._values["right_columns"] = right_columns
            if sample_size is not None:
                self._values["sample_size"] = sample_size
            if sample_type is not None:
                self._values["sample_type"] = sample_type
            if secondary_inputs is not None:
                self._values["secondary_inputs"] = secondary_inputs
            if second_input is not None:
                self._values["second_input"] = second_input
            if sheet_indexes is not None:
                self._values["sheet_indexes"] = sheet_indexes
            if sheet_names is not None:
                self._values["sheet_names"] = sheet_names
            if source_column is not None:
                self._values["source_column"] = source_column
            if source_column1 is not None:
                self._values["source_column1"] = source_column1
            if source_column2 is not None:
                self._values["source_column2"] = source_column2
            if source_columns is not None:
                self._values["source_columns"] = source_columns
            if start_column_index is not None:
                self._values["start_column_index"] = start_column_index
            if start_pattern is not None:
                self._values["start_pattern"] = start_pattern
            if start_position is not None:
                self._values["start_position"] = start_position
            if start_value is not None:
                self._values["start_value"] = start_value
            if stemming_mode is not None:
                self._values["stemming_mode"] = stemming_mode
            if step_count is not None:
                self._values["step_count"] = step_count
            if step_index is not None:
                self._values["step_index"] = step_index
            if stop_words_mode is not None:
                self._values["stop_words_mode"] = stop_words_mode
            if strategy is not None:
                self._values["strategy"] = strategy
            if target_column is not None:
                self._values["target_column"] = target_column
            if target_column_names is not None:
                self._values["target_column_names"] = target_column_names
            if target_date_format is not None:
                self._values["target_date_format"] = target_date_format
            if target_index is not None:
                self._values["target_index"] = target_index
            if time_zone is not None:
                self._values["time_zone"] = time_zone
            if tokenizer_pattern is not None:
                self._values["tokenizer_pattern"] = tokenizer_pattern
            if true_string is not None:
                self._values["true_string"] = true_string
            if udf_lang is not None:
                self._values["udf_lang"] = udf_lang
            if units is not None:
                self._values["units"] = units
            if unpivot_column is not None:
                self._values["unpivot_column"] = unpivot_column
            if upper_bound is not None:
                self._values["upper_bound"] = upper_bound
            if use_new_data_frame is not None:
                self._values["use_new_data_frame"] = use_new_data_frame
            if value is not None:
                self._values["value"] = value
            if value1 is not None:
                self._values["value1"] = value1
            if value2 is not None:
                self._values["value2"] = value2
            if value_column is not None:
                self._values["value_column"] = value_column
            if view_frame is not None:
                self._values["view_frame"] = view_frame

        @builtins.property
        def aggregate_function(self) -> typing.Optional[builtins.str]:
            """``CfnRecipe.RecipeParametersProperty.AggregateFunction``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipeparameters.html#cfn-databrew-recipe-recipeparameters-aggregatefunction
            """
            result = self._values.get("aggregate_function")
            return result

        @builtins.property
        def base(self) -> typing.Optional[builtins.str]:
            """``CfnRecipe.RecipeParametersProperty.Base``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipeparameters.html#cfn-databrew-recipe-recipeparameters-base
            """
            result = self._values.get("base")
            return result

        @builtins.property
        def case_statement(self) -> typing.Optional[builtins.str]:
            """``CfnRecipe.RecipeParametersProperty.CaseStatement``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipeparameters.html#cfn-databrew-recipe-recipeparameters-casestatement
            """
            result = self._values.get("case_statement")
            return result

        @builtins.property
        def category_map(self) -> typing.Optional[builtins.str]:
            """``CfnRecipe.RecipeParametersProperty.CategoryMap``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipeparameters.html#cfn-databrew-recipe-recipeparameters-categorymap
            """
            result = self._values.get("category_map")
            return result

        @builtins.property
        def chars_to_remove(self) -> typing.Optional[builtins.str]:
            """``CfnRecipe.RecipeParametersProperty.CharsToRemove``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipeparameters.html#cfn-databrew-recipe-recipeparameters-charstoremove
            """
            result = self._values.get("chars_to_remove")
            return result

        @builtins.property
        def collapse_consecutive_whitespace(self) -> typing.Optional[builtins.str]:
            """``CfnRecipe.RecipeParametersProperty.CollapseConsecutiveWhitespace``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipeparameters.html#cfn-databrew-recipe-recipeparameters-collapseconsecutivewhitespace
            """
            result = self._values.get("collapse_consecutive_whitespace")
            return result

        @builtins.property
        def column_data_type(self) -> typing.Optional[builtins.str]:
            """``CfnRecipe.RecipeParametersProperty.ColumnDataType``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipeparameters.html#cfn-databrew-recipe-recipeparameters-columndatatype
            """
            result = self._values.get("column_data_type")
            return result

        @builtins.property
        def column_range(self) -> typing.Optional[builtins.str]:
            """``CfnRecipe.RecipeParametersProperty.ColumnRange``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipeparameters.html#cfn-databrew-recipe-recipeparameters-columnrange
            """
            result = self._values.get("column_range")
            return result

        @builtins.property
        def count(self) -> typing.Optional[builtins.str]:
            """``CfnRecipe.RecipeParametersProperty.Count``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipeparameters.html#cfn-databrew-recipe-recipeparameters-count
            """
            result = self._values.get("count")
            return result

        @builtins.property
        def custom_characters(self) -> typing.Optional[builtins.str]:
            """``CfnRecipe.RecipeParametersProperty.CustomCharacters``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipeparameters.html#cfn-databrew-recipe-recipeparameters-customcharacters
            """
            result = self._values.get("custom_characters")
            return result

        @builtins.property
        def custom_stop_words(self) -> typing.Optional[builtins.str]:
            """``CfnRecipe.RecipeParametersProperty.CustomStopWords``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipeparameters.html#cfn-databrew-recipe-recipeparameters-customstopwords
            """
            result = self._values.get("custom_stop_words")
            return result

        @builtins.property
        def custom_value(self) -> typing.Optional[builtins.str]:
            """``CfnRecipe.RecipeParametersProperty.CustomValue``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipeparameters.html#cfn-databrew-recipe-recipeparameters-customvalue
            """
            result = self._values.get("custom_value")
            return result

        @builtins.property
        def datasets_columns(self) -> typing.Optional[builtins.str]:
            """``CfnRecipe.RecipeParametersProperty.DatasetsColumns``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipeparameters.html#cfn-databrew-recipe-recipeparameters-datasetscolumns
            """
            result = self._values.get("datasets_columns")
            return result

        @builtins.property
        def date_add_value(self) -> typing.Optional[builtins.str]:
            """``CfnRecipe.RecipeParametersProperty.DateAddValue``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipeparameters.html#cfn-databrew-recipe-recipeparameters-dateaddvalue
            """
            result = self._values.get("date_add_value")
            return result

        @builtins.property
        def date_time_format(self) -> typing.Optional[builtins.str]:
            """``CfnRecipe.RecipeParametersProperty.DateTimeFormat``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipeparameters.html#cfn-databrew-recipe-recipeparameters-datetimeformat
            """
            result = self._values.get("date_time_format")
            return result

        @builtins.property
        def date_time_parameters(self) -> typing.Optional[builtins.str]:
            """``CfnRecipe.RecipeParametersProperty.DateTimeParameters``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipeparameters.html#cfn-databrew-recipe-recipeparameters-datetimeparameters
            """
            result = self._values.get("date_time_parameters")
            return result

        @builtins.property
        def delete_other_rows(self) -> typing.Optional[builtins.str]:
            """``CfnRecipe.RecipeParametersProperty.DeleteOtherRows``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipeparameters.html#cfn-databrew-recipe-recipeparameters-deleteotherrows
            """
            result = self._values.get("delete_other_rows")
            return result

        @builtins.property
        def delimiter(self) -> typing.Optional[builtins.str]:
            """``CfnRecipe.RecipeParametersProperty.Delimiter``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipeparameters.html#cfn-databrew-recipe-recipeparameters-delimiter
            """
            result = self._values.get("delimiter")
            return result

        @builtins.property
        def end_pattern(self) -> typing.Optional[builtins.str]:
            """``CfnRecipe.RecipeParametersProperty.EndPattern``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipeparameters.html#cfn-databrew-recipe-recipeparameters-endpattern
            """
            result = self._values.get("end_pattern")
            return result

        @builtins.property
        def end_position(self) -> typing.Optional[builtins.str]:
            """``CfnRecipe.RecipeParametersProperty.EndPosition``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipeparameters.html#cfn-databrew-recipe-recipeparameters-endposition
            """
            result = self._values.get("end_position")
            return result

        @builtins.property
        def end_value(self) -> typing.Optional[builtins.str]:
            """``CfnRecipe.RecipeParametersProperty.EndValue``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipeparameters.html#cfn-databrew-recipe-recipeparameters-endvalue
            """
            result = self._values.get("end_value")
            return result

        @builtins.property
        def expand_contractions(self) -> typing.Optional[builtins.str]:
            """``CfnRecipe.RecipeParametersProperty.ExpandContractions``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipeparameters.html#cfn-databrew-recipe-recipeparameters-expandcontractions
            """
            result = self._values.get("expand_contractions")
            return result

        @builtins.property
        def exponent(self) -> typing.Optional[builtins.str]:
            """``CfnRecipe.RecipeParametersProperty.Exponent``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipeparameters.html#cfn-databrew-recipe-recipeparameters-exponent
            """
            result = self._values.get("exponent")
            return result

        @builtins.property
        def false_string(self) -> typing.Optional[builtins.str]:
            """``CfnRecipe.RecipeParametersProperty.FalseString``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipeparameters.html#cfn-databrew-recipe-recipeparameters-falsestring
            """
            result = self._values.get("false_string")
            return result

        @builtins.property
        def group_by_agg_function_options(self) -> typing.Optional[builtins.str]:
            """``CfnRecipe.RecipeParametersProperty.GroupByAggFunctionOptions``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipeparameters.html#cfn-databrew-recipe-recipeparameters-groupbyaggfunctionoptions
            """
            result = self._values.get("group_by_agg_function_options")
            return result

        @builtins.property
        def group_by_columns(self) -> typing.Optional[builtins.str]:
            """``CfnRecipe.RecipeParametersProperty.GroupByColumns``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipeparameters.html#cfn-databrew-recipe-recipeparameters-groupbycolumns
            """
            result = self._values.get("group_by_columns")
            return result

        @builtins.property
        def hidden_columns(self) -> typing.Optional[builtins.str]:
            """``CfnRecipe.RecipeParametersProperty.HiddenColumns``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipeparameters.html#cfn-databrew-recipe-recipeparameters-hiddencolumns
            """
            result = self._values.get("hidden_columns")
            return result

        @builtins.property
        def ignore_case(self) -> typing.Optional[builtins.str]:
            """``CfnRecipe.RecipeParametersProperty.IgnoreCase``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipeparameters.html#cfn-databrew-recipe-recipeparameters-ignorecase
            """
            result = self._values.get("ignore_case")
            return result

        @builtins.property
        def include_in_split(self) -> typing.Optional[builtins.str]:
            """``CfnRecipe.RecipeParametersProperty.IncludeInSplit``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipeparameters.html#cfn-databrew-recipe-recipeparameters-includeinsplit
            """
            result = self._values.get("include_in_split")
            return result

        @builtins.property
        def input(self) -> typing.Any:
            """``CfnRecipe.RecipeParametersProperty.Input``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipeparameters.html#cfn-databrew-recipe-recipeparameters-input
            """
            result = self._values.get("input")
            return result

        @builtins.property
        def interval(self) -> typing.Optional[builtins.str]:
            """``CfnRecipe.RecipeParametersProperty.Interval``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipeparameters.html#cfn-databrew-recipe-recipeparameters-interval
            """
            result = self._values.get("interval")
            return result

        @builtins.property
        def is_text(self) -> typing.Optional[builtins.str]:
            """``CfnRecipe.RecipeParametersProperty.IsText``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipeparameters.html#cfn-databrew-recipe-recipeparameters-istext
            """
            result = self._values.get("is_text")
            return result

        @builtins.property
        def join_keys(self) -> typing.Optional[builtins.str]:
            """``CfnRecipe.RecipeParametersProperty.JoinKeys``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipeparameters.html#cfn-databrew-recipe-recipeparameters-joinkeys
            """
            result = self._values.get("join_keys")
            return result

        @builtins.property
        def join_type(self) -> typing.Optional[builtins.str]:
            """``CfnRecipe.RecipeParametersProperty.JoinType``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipeparameters.html#cfn-databrew-recipe-recipeparameters-jointype
            """
            result = self._values.get("join_type")
            return result

        @builtins.property
        def left_columns(self) -> typing.Optional[builtins.str]:
            """``CfnRecipe.RecipeParametersProperty.LeftColumns``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipeparameters.html#cfn-databrew-recipe-recipeparameters-leftcolumns
            """
            result = self._values.get("left_columns")
            return result

        @builtins.property
        def limit(self) -> typing.Optional[builtins.str]:
            """``CfnRecipe.RecipeParametersProperty.Limit``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipeparameters.html#cfn-databrew-recipe-recipeparameters-limit
            """
            result = self._values.get("limit")
            return result

        @builtins.property
        def lower_bound(self) -> typing.Optional[builtins.str]:
            """``CfnRecipe.RecipeParametersProperty.LowerBound``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipeparameters.html#cfn-databrew-recipe-recipeparameters-lowerbound
            """
            result = self._values.get("lower_bound")
            return result

        @builtins.property
        def map_type(self) -> typing.Optional[builtins.str]:
            """``CfnRecipe.RecipeParametersProperty.MapType``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipeparameters.html#cfn-databrew-recipe-recipeparameters-maptype
            """
            result = self._values.get("map_type")
            return result

        @builtins.property
        def mode_type(self) -> typing.Optional[builtins.str]:
            """``CfnRecipe.RecipeParametersProperty.ModeType``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipeparameters.html#cfn-databrew-recipe-recipeparameters-modetype
            """
            result = self._values.get("mode_type")
            return result

        @builtins.property
        def multi_line(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
            """``CfnRecipe.RecipeParametersProperty.MultiLine``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipeparameters.html#cfn-databrew-recipe-recipeparameters-multiline
            """
            result = self._values.get("multi_line")
            return result

        @builtins.property
        def num_rows(self) -> typing.Optional[builtins.str]:
            """``CfnRecipe.RecipeParametersProperty.NumRows``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipeparameters.html#cfn-databrew-recipe-recipeparameters-numrows
            """
            result = self._values.get("num_rows")
            return result

        @builtins.property
        def num_rows_after(self) -> typing.Optional[builtins.str]:
            """``CfnRecipe.RecipeParametersProperty.NumRowsAfter``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipeparameters.html#cfn-databrew-recipe-recipeparameters-numrowsafter
            """
            result = self._values.get("num_rows_after")
            return result

        @builtins.property
        def num_rows_before(self) -> typing.Optional[builtins.str]:
            """``CfnRecipe.RecipeParametersProperty.NumRowsBefore``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipeparameters.html#cfn-databrew-recipe-recipeparameters-numrowsbefore
            """
            result = self._values.get("num_rows_before")
            return result

        @builtins.property
        def order_by_column(self) -> typing.Optional[builtins.str]:
            """``CfnRecipe.RecipeParametersProperty.OrderByColumn``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipeparameters.html#cfn-databrew-recipe-recipeparameters-orderbycolumn
            """
            result = self._values.get("order_by_column")
            return result

        @builtins.property
        def order_by_columns(self) -> typing.Optional[builtins.str]:
            """``CfnRecipe.RecipeParametersProperty.OrderByColumns``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipeparameters.html#cfn-databrew-recipe-recipeparameters-orderbycolumns
            """
            result = self._values.get("order_by_columns")
            return result

        @builtins.property
        def other(self) -> typing.Optional[builtins.str]:
            """``CfnRecipe.RecipeParametersProperty.Other``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipeparameters.html#cfn-databrew-recipe-recipeparameters-other
            """
            result = self._values.get("other")
            return result

        @builtins.property
        def pattern(self) -> typing.Optional[builtins.str]:
            """``CfnRecipe.RecipeParametersProperty.Pattern``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipeparameters.html#cfn-databrew-recipe-recipeparameters-pattern
            """
            result = self._values.get("pattern")
            return result

        @builtins.property
        def pattern_option1(self) -> typing.Optional[builtins.str]:
            """``CfnRecipe.RecipeParametersProperty.PatternOption1``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipeparameters.html#cfn-databrew-recipe-recipeparameters-patternoption1
            """
            result = self._values.get("pattern_option1")
            return result

        @builtins.property
        def pattern_option2(self) -> typing.Optional[builtins.str]:
            """``CfnRecipe.RecipeParametersProperty.PatternOption2``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipeparameters.html#cfn-databrew-recipe-recipeparameters-patternoption2
            """
            result = self._values.get("pattern_option2")
            return result

        @builtins.property
        def pattern_options(self) -> typing.Optional[builtins.str]:
            """``CfnRecipe.RecipeParametersProperty.PatternOptions``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipeparameters.html#cfn-databrew-recipe-recipeparameters-patternoptions
            """
            result = self._values.get("pattern_options")
            return result

        @builtins.property
        def period(self) -> typing.Optional[builtins.str]:
            """``CfnRecipe.RecipeParametersProperty.Period``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipeparameters.html#cfn-databrew-recipe-recipeparameters-period
            """
            result = self._values.get("period")
            return result

        @builtins.property
        def position(self) -> typing.Optional[builtins.str]:
            """``CfnRecipe.RecipeParametersProperty.Position``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipeparameters.html#cfn-databrew-recipe-recipeparameters-position
            """
            result = self._values.get("position")
            return result

        @builtins.property
        def remove_all_punctuation(self) -> typing.Optional[builtins.str]:
            """``CfnRecipe.RecipeParametersProperty.RemoveAllPunctuation``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipeparameters.html#cfn-databrew-recipe-recipeparameters-removeallpunctuation
            """
            result = self._values.get("remove_all_punctuation")
            return result

        @builtins.property
        def remove_all_quotes(self) -> typing.Optional[builtins.str]:
            """``CfnRecipe.RecipeParametersProperty.RemoveAllQuotes``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipeparameters.html#cfn-databrew-recipe-recipeparameters-removeallquotes
            """
            result = self._values.get("remove_all_quotes")
            return result

        @builtins.property
        def remove_all_whitespace(self) -> typing.Optional[builtins.str]:
            """``CfnRecipe.RecipeParametersProperty.RemoveAllWhitespace``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipeparameters.html#cfn-databrew-recipe-recipeparameters-removeallwhitespace
            """
            result = self._values.get("remove_all_whitespace")
            return result

        @builtins.property
        def remove_custom_characters(self) -> typing.Optional[builtins.str]:
            """``CfnRecipe.RecipeParametersProperty.RemoveCustomCharacters``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipeparameters.html#cfn-databrew-recipe-recipeparameters-removecustomcharacters
            """
            result = self._values.get("remove_custom_characters")
            return result

        @builtins.property
        def remove_custom_value(self) -> typing.Optional[builtins.str]:
            """``CfnRecipe.RecipeParametersProperty.RemoveCustomValue``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipeparameters.html#cfn-databrew-recipe-recipeparameters-removecustomvalue
            """
            result = self._values.get("remove_custom_value")
            return result

        @builtins.property
        def remove_leading_and_trailing_punctuation(
            self,
        ) -> typing.Optional[builtins.str]:
            """``CfnRecipe.RecipeParametersProperty.RemoveLeadingAndTrailingPunctuation``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipeparameters.html#cfn-databrew-recipe-recipeparameters-removeleadingandtrailingpunctuation
            """
            result = self._values.get("remove_leading_and_trailing_punctuation")
            return result

        @builtins.property
        def remove_leading_and_trailing_quotes(self) -> typing.Optional[builtins.str]:
            """``CfnRecipe.RecipeParametersProperty.RemoveLeadingAndTrailingQuotes``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipeparameters.html#cfn-databrew-recipe-recipeparameters-removeleadingandtrailingquotes
            """
            result = self._values.get("remove_leading_and_trailing_quotes")
            return result

        @builtins.property
        def remove_leading_and_trailing_whitespace(
            self,
        ) -> typing.Optional[builtins.str]:
            """``CfnRecipe.RecipeParametersProperty.RemoveLeadingAndTrailingWhitespace``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipeparameters.html#cfn-databrew-recipe-recipeparameters-removeleadingandtrailingwhitespace
            """
            result = self._values.get("remove_leading_and_trailing_whitespace")
            return result

        @builtins.property
        def remove_letters(self) -> typing.Optional[builtins.str]:
            """``CfnRecipe.RecipeParametersProperty.RemoveLetters``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipeparameters.html#cfn-databrew-recipe-recipeparameters-removeletters
            """
            result = self._values.get("remove_letters")
            return result

        @builtins.property
        def remove_numbers(self) -> typing.Optional[builtins.str]:
            """``CfnRecipe.RecipeParametersProperty.RemoveNumbers``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipeparameters.html#cfn-databrew-recipe-recipeparameters-removenumbers
            """
            result = self._values.get("remove_numbers")
            return result

        @builtins.property
        def remove_source_column(self) -> typing.Optional[builtins.str]:
            """``CfnRecipe.RecipeParametersProperty.RemoveSourceColumn``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipeparameters.html#cfn-databrew-recipe-recipeparameters-removesourcecolumn
            """
            result = self._values.get("remove_source_column")
            return result

        @builtins.property
        def remove_special_characters(self) -> typing.Optional[builtins.str]:
            """``CfnRecipe.RecipeParametersProperty.RemoveSpecialCharacters``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipeparameters.html#cfn-databrew-recipe-recipeparameters-removespecialcharacters
            """
            result = self._values.get("remove_special_characters")
            return result

        @builtins.property
        def right_columns(self) -> typing.Optional[builtins.str]:
            """``CfnRecipe.RecipeParametersProperty.RightColumns``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipeparameters.html#cfn-databrew-recipe-recipeparameters-rightcolumns
            """
            result = self._values.get("right_columns")
            return result

        @builtins.property
        def sample_size(self) -> typing.Optional[builtins.str]:
            """``CfnRecipe.RecipeParametersProperty.SampleSize``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipeparameters.html#cfn-databrew-recipe-recipeparameters-samplesize
            """
            result = self._values.get("sample_size")
            return result

        @builtins.property
        def sample_type(self) -> typing.Optional[builtins.str]:
            """``CfnRecipe.RecipeParametersProperty.SampleType``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipeparameters.html#cfn-databrew-recipe-recipeparameters-sampletype
            """
            result = self._values.get("sample_type")
            return result

        @builtins.property
        def secondary_inputs(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnRecipe.SecondaryInputProperty"]]]]:
            """``CfnRecipe.RecipeParametersProperty.SecondaryInputs``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipeparameters.html#cfn-databrew-recipe-recipeparameters-secondaryinputs
            """
            result = self._values.get("secondary_inputs")
            return result

        @builtins.property
        def second_input(self) -> typing.Optional[builtins.str]:
            """``CfnRecipe.RecipeParametersProperty.SecondInput``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipeparameters.html#cfn-databrew-recipe-recipeparameters-secondinput
            """
            result = self._values.get("second_input")
            return result

        @builtins.property
        def sheet_indexes(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[jsii.Number]]]:
            """``CfnRecipe.RecipeParametersProperty.SheetIndexes``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipeparameters.html#cfn-databrew-recipe-recipeparameters-sheetindexes
            """
            result = self._values.get("sheet_indexes")
            return result

        @builtins.property
        def sheet_names(self) -> typing.Optional[typing.List[builtins.str]]:
            """``CfnRecipe.RecipeParametersProperty.SheetNames``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipeparameters.html#cfn-databrew-recipe-recipeparameters-sheetnames
            """
            result = self._values.get("sheet_names")
            return result

        @builtins.property
        def source_column(self) -> typing.Optional[builtins.str]:
            """``CfnRecipe.RecipeParametersProperty.SourceColumn``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipeparameters.html#cfn-databrew-recipe-recipeparameters-sourcecolumn
            """
            result = self._values.get("source_column")
            return result

        @builtins.property
        def source_column1(self) -> typing.Optional[builtins.str]:
            """``CfnRecipe.RecipeParametersProperty.SourceColumn1``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipeparameters.html#cfn-databrew-recipe-recipeparameters-sourcecolumn1
            """
            result = self._values.get("source_column1")
            return result

        @builtins.property
        def source_column2(self) -> typing.Optional[builtins.str]:
            """``CfnRecipe.RecipeParametersProperty.SourceColumn2``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipeparameters.html#cfn-databrew-recipe-recipeparameters-sourcecolumn2
            """
            result = self._values.get("source_column2")
            return result

        @builtins.property
        def source_columns(self) -> typing.Optional[builtins.str]:
            """``CfnRecipe.RecipeParametersProperty.SourceColumns``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipeparameters.html#cfn-databrew-recipe-recipeparameters-sourcecolumns
            """
            result = self._values.get("source_columns")
            return result

        @builtins.property
        def start_column_index(self) -> typing.Optional[builtins.str]:
            """``CfnRecipe.RecipeParametersProperty.StartColumnIndex``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipeparameters.html#cfn-databrew-recipe-recipeparameters-startcolumnindex
            """
            result = self._values.get("start_column_index")
            return result

        @builtins.property
        def start_pattern(self) -> typing.Optional[builtins.str]:
            """``CfnRecipe.RecipeParametersProperty.StartPattern``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipeparameters.html#cfn-databrew-recipe-recipeparameters-startpattern
            """
            result = self._values.get("start_pattern")
            return result

        @builtins.property
        def start_position(self) -> typing.Optional[builtins.str]:
            """``CfnRecipe.RecipeParametersProperty.StartPosition``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipeparameters.html#cfn-databrew-recipe-recipeparameters-startposition
            """
            result = self._values.get("start_position")
            return result

        @builtins.property
        def start_value(self) -> typing.Optional[builtins.str]:
            """``CfnRecipe.RecipeParametersProperty.StartValue``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipeparameters.html#cfn-databrew-recipe-recipeparameters-startvalue
            """
            result = self._values.get("start_value")
            return result

        @builtins.property
        def stemming_mode(self) -> typing.Optional[builtins.str]:
            """``CfnRecipe.RecipeParametersProperty.StemmingMode``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipeparameters.html#cfn-databrew-recipe-recipeparameters-stemmingmode
            """
            result = self._values.get("stemming_mode")
            return result

        @builtins.property
        def step_count(self) -> typing.Optional[builtins.str]:
            """``CfnRecipe.RecipeParametersProperty.StepCount``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipeparameters.html#cfn-databrew-recipe-recipeparameters-stepcount
            """
            result = self._values.get("step_count")
            return result

        @builtins.property
        def step_index(self) -> typing.Optional[builtins.str]:
            """``CfnRecipe.RecipeParametersProperty.StepIndex``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipeparameters.html#cfn-databrew-recipe-recipeparameters-stepindex
            """
            result = self._values.get("step_index")
            return result

        @builtins.property
        def stop_words_mode(self) -> typing.Optional[builtins.str]:
            """``CfnRecipe.RecipeParametersProperty.StopWordsMode``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipeparameters.html#cfn-databrew-recipe-recipeparameters-stopwordsmode
            """
            result = self._values.get("stop_words_mode")
            return result

        @builtins.property
        def strategy(self) -> typing.Optional[builtins.str]:
            """``CfnRecipe.RecipeParametersProperty.Strategy``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipeparameters.html#cfn-databrew-recipe-recipeparameters-strategy
            """
            result = self._values.get("strategy")
            return result

        @builtins.property
        def target_column(self) -> typing.Optional[builtins.str]:
            """``CfnRecipe.RecipeParametersProperty.TargetColumn``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipeparameters.html#cfn-databrew-recipe-recipeparameters-targetcolumn
            """
            result = self._values.get("target_column")
            return result

        @builtins.property
        def target_column_names(self) -> typing.Optional[builtins.str]:
            """``CfnRecipe.RecipeParametersProperty.TargetColumnNames``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipeparameters.html#cfn-databrew-recipe-recipeparameters-targetcolumnnames
            """
            result = self._values.get("target_column_names")
            return result

        @builtins.property
        def target_date_format(self) -> typing.Optional[builtins.str]:
            """``CfnRecipe.RecipeParametersProperty.TargetDateFormat``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipeparameters.html#cfn-databrew-recipe-recipeparameters-targetdateformat
            """
            result = self._values.get("target_date_format")
            return result

        @builtins.property
        def target_index(self) -> typing.Optional[builtins.str]:
            """``CfnRecipe.RecipeParametersProperty.TargetIndex``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipeparameters.html#cfn-databrew-recipe-recipeparameters-targetindex
            """
            result = self._values.get("target_index")
            return result

        @builtins.property
        def time_zone(self) -> typing.Optional[builtins.str]:
            """``CfnRecipe.RecipeParametersProperty.TimeZone``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipeparameters.html#cfn-databrew-recipe-recipeparameters-timezone
            """
            result = self._values.get("time_zone")
            return result

        @builtins.property
        def tokenizer_pattern(self) -> typing.Optional[builtins.str]:
            """``CfnRecipe.RecipeParametersProperty.TokenizerPattern``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipeparameters.html#cfn-databrew-recipe-recipeparameters-tokenizerpattern
            """
            result = self._values.get("tokenizer_pattern")
            return result

        @builtins.property
        def true_string(self) -> typing.Optional[builtins.str]:
            """``CfnRecipe.RecipeParametersProperty.TrueString``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipeparameters.html#cfn-databrew-recipe-recipeparameters-truestring
            """
            result = self._values.get("true_string")
            return result

        @builtins.property
        def udf_lang(self) -> typing.Optional[builtins.str]:
            """``CfnRecipe.RecipeParametersProperty.UdfLang``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipeparameters.html#cfn-databrew-recipe-recipeparameters-udflang
            """
            result = self._values.get("udf_lang")
            return result

        @builtins.property
        def units(self) -> typing.Optional[builtins.str]:
            """``CfnRecipe.RecipeParametersProperty.Units``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipeparameters.html#cfn-databrew-recipe-recipeparameters-units
            """
            result = self._values.get("units")
            return result

        @builtins.property
        def unpivot_column(self) -> typing.Optional[builtins.str]:
            """``CfnRecipe.RecipeParametersProperty.UnpivotColumn``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipeparameters.html#cfn-databrew-recipe-recipeparameters-unpivotcolumn
            """
            result = self._values.get("unpivot_column")
            return result

        @builtins.property
        def upper_bound(self) -> typing.Optional[builtins.str]:
            """``CfnRecipe.RecipeParametersProperty.UpperBound``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipeparameters.html#cfn-databrew-recipe-recipeparameters-upperbound
            """
            result = self._values.get("upper_bound")
            return result

        @builtins.property
        def use_new_data_frame(self) -> typing.Optional[builtins.str]:
            """``CfnRecipe.RecipeParametersProperty.UseNewDataFrame``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipeparameters.html#cfn-databrew-recipe-recipeparameters-usenewdataframe
            """
            result = self._values.get("use_new_data_frame")
            return result

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            """``CfnRecipe.RecipeParametersProperty.Value``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipeparameters.html#cfn-databrew-recipe-recipeparameters-value
            """
            result = self._values.get("value")
            return result

        @builtins.property
        def value1(self) -> typing.Optional[builtins.str]:
            """``CfnRecipe.RecipeParametersProperty.Value1``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipeparameters.html#cfn-databrew-recipe-recipeparameters-value1
            """
            result = self._values.get("value1")
            return result

        @builtins.property
        def value2(self) -> typing.Optional[builtins.str]:
            """``CfnRecipe.RecipeParametersProperty.Value2``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipeparameters.html#cfn-databrew-recipe-recipeparameters-value2
            """
            result = self._values.get("value2")
            return result

        @builtins.property
        def value_column(self) -> typing.Optional[builtins.str]:
            """``CfnRecipe.RecipeParametersProperty.ValueColumn``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipeparameters.html#cfn-databrew-recipe-recipeparameters-valuecolumn
            """
            result = self._values.get("value_column")
            return result

        @builtins.property
        def view_frame(self) -> typing.Optional[builtins.str]:
            """``CfnRecipe.RecipeParametersProperty.ViewFrame``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipeparameters.html#cfn-databrew-recipe-recipeparameters-viewframe
            """
            result = self._values.get("view_frame")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RecipeParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-databrew.CfnRecipe.RecipeStepProperty",
        jsii_struct_bases=[],
        name_mapping={
            "action": "action",
            "condition_expressions": "conditionExpressions",
        },
    )
    class RecipeStepProperty:
        def __init__(
            self,
            *,
            action: typing.Union[aws_cdk.core.IResolvable, "CfnRecipe.ActionProperty"],
            condition_expressions: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnRecipe.ConditionExpressionProperty"]]]] = None,
        ) -> None:
            """
            :param action: ``CfnRecipe.RecipeStepProperty.Action``.
            :param condition_expressions: ``CfnRecipe.RecipeStepProperty.ConditionExpressions``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipestep.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "action": action,
            }
            if condition_expressions is not None:
                self._values["condition_expressions"] = condition_expressions

        @builtins.property
        def action(
            self,
        ) -> typing.Union[aws_cdk.core.IResolvable, "CfnRecipe.ActionProperty"]:
            """``CfnRecipe.RecipeStepProperty.Action``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipestep.html#cfn-databrew-recipe-recipestep-action
            """
            result = self._values.get("action")
            assert result is not None, "Required property 'action' is missing"
            return result

        @builtins.property
        def condition_expressions(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnRecipe.ConditionExpressionProperty"]]]]:
            """``CfnRecipe.RecipeStepProperty.ConditionExpressions``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipestep.html#cfn-databrew-recipe-recipestep-conditionexpressions
            """
            result = self._values.get("condition_expressions")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RecipeStepProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-databrew.CfnRecipe.S3LocationProperty",
        jsii_struct_bases=[],
        name_mapping={"bucket": "bucket", "key": "key"},
    )
    class S3LocationProperty:
        def __init__(
            self,
            *,
            bucket: builtins.str,
            key: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param bucket: ``CfnRecipe.S3LocationProperty.Bucket``.
            :param key: ``CfnRecipe.S3LocationProperty.Key``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-s3location.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "bucket": bucket,
            }
            if key is not None:
                self._values["key"] = key

        @builtins.property
        def bucket(self) -> builtins.str:
            """``CfnRecipe.S3LocationProperty.Bucket``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-s3location.html#cfn-databrew-recipe-s3location-bucket
            """
            result = self._values.get("bucket")
            assert result is not None, "Required property 'bucket' is missing"
            return result

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            """``CfnRecipe.S3LocationProperty.Key``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-s3location.html#cfn-databrew-recipe-s3location-key
            """
            result = self._values.get("key")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3LocationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-databrew.CfnRecipe.SecondaryInputProperty",
        jsii_struct_bases=[],
        name_mapping={
            "data_catalog_input_definition": "dataCatalogInputDefinition",
            "s3_input_definition": "s3InputDefinition",
        },
    )
    class SecondaryInputProperty:
        def __init__(
            self,
            *,
            data_catalog_input_definition: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRecipe.DataCatalogInputDefinitionProperty"]] = None,
            s3_input_definition: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRecipe.S3LocationProperty"]] = None,
        ) -> None:
            """
            :param data_catalog_input_definition: ``CfnRecipe.SecondaryInputProperty.DataCatalogInputDefinition``.
            :param s3_input_definition: ``CfnRecipe.SecondaryInputProperty.S3InputDefinition``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-secondaryinput.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if data_catalog_input_definition is not None:
                self._values["data_catalog_input_definition"] = data_catalog_input_definition
            if s3_input_definition is not None:
                self._values["s3_input_definition"] = s3_input_definition

        @builtins.property
        def data_catalog_input_definition(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRecipe.DataCatalogInputDefinitionProperty"]]:
            """``CfnRecipe.SecondaryInputProperty.DataCatalogInputDefinition``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-secondaryinput.html#cfn-databrew-recipe-secondaryinput-datacataloginputdefinition
            """
            result = self._values.get("data_catalog_input_definition")
            return result

        @builtins.property
        def s3_input_definition(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRecipe.S3LocationProperty"]]:
            """``CfnRecipe.SecondaryInputProperty.S3InputDefinition``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-secondaryinput.html#cfn-databrew-recipe-secondaryinput-s3inputdefinition
            """
            result = self._values.get("s3_input_definition")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SecondaryInputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-databrew.CfnRecipeProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "steps": "steps",
        "description": "description",
        "tags": "tags",
    },
)
class CfnRecipeProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        steps: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnRecipe.RecipeStepProperty]]],
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]] = None,
    ) -> None:
        """Properties for defining a ``AWS::DataBrew::Recipe``.

        :param name: ``AWS::DataBrew::Recipe.Name``.
        :param steps: ``AWS::DataBrew::Recipe.Steps``.
        :param description: ``AWS::DataBrew::Recipe.Description``.
        :param tags: ``AWS::DataBrew::Recipe.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-recipe.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "name": name,
            "steps": steps,
        }
        if description is not None:
            self._values["description"] = description
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def name(self) -> builtins.str:
        """``AWS::DataBrew::Recipe.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-recipe.html#cfn-databrew-recipe-name
        """
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return result

    @builtins.property
    def steps(
        self,
    ) -> typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnRecipe.RecipeStepProperty]]]:
        """``AWS::DataBrew::Recipe.Steps``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-recipe.html#cfn-databrew-recipe-steps
        """
        result = self._values.get("steps")
        assert result is not None, "Required property 'steps' is missing"
        return result

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        """``AWS::DataBrew::Recipe.Description``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-recipe.html#cfn-databrew-recipe-description
        """
        result = self._values.get("description")
        return result

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        """``AWS::DataBrew::Recipe.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-recipe.html#cfn-databrew-recipe-tags
        """
        result = self._values.get("tags")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnRecipeProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnSchedule(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-databrew.CfnSchedule",
):
    """A CloudFormation ``AWS::DataBrew::Schedule``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-schedule.html
    :cloudformationResource: AWS::DataBrew::Schedule
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        cron_expression: builtins.str,
        name: builtins.str,
        job_names: typing.Optional[typing.List[builtins.str]] = None,
        tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]] = None,
    ) -> None:
        """Create a new ``AWS::DataBrew::Schedule``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param cron_expression: ``AWS::DataBrew::Schedule.CronExpression``.
        :param name: ``AWS::DataBrew::Schedule.Name``.
        :param job_names: ``AWS::DataBrew::Schedule.JobNames``.
        :param tags: ``AWS::DataBrew::Schedule.Tags``.
        """
        props = CfnScheduleProps(
            cron_expression=cron_expression, name=name, job_names=job_names, tags=tags
        )

        jsii.create(CfnSchedule, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        """(experimental) Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        """``AWS::DataBrew::Schedule.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-schedule.html#cfn-databrew-schedule-tags
        """
        return jsii.get(self, "tags")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cronExpression")
    def cron_expression(self) -> builtins.str:
        """``AWS::DataBrew::Schedule.CronExpression``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-schedule.html#cfn-databrew-schedule-cronexpression
        """
        return jsii.get(self, "cronExpression")

    @cron_expression.setter # type: ignore
    def cron_expression(self, value: builtins.str) -> None:
        jsii.set(self, "cronExpression", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        """``AWS::DataBrew::Schedule.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-schedule.html#cfn-databrew-schedule-name
        """
        return jsii.get(self, "name")

    @name.setter # type: ignore
    def name(self, value: builtins.str) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="jobNames")
    def job_names(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::DataBrew::Schedule.JobNames``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-schedule.html#cfn-databrew-schedule-jobnames
        """
        return jsii.get(self, "jobNames")

    @job_names.setter # type: ignore
    def job_names(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        jsii.set(self, "jobNames", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-databrew.CfnScheduleProps",
    jsii_struct_bases=[],
    name_mapping={
        "cron_expression": "cronExpression",
        "name": "name",
        "job_names": "jobNames",
        "tags": "tags",
    },
)
class CfnScheduleProps:
    def __init__(
        self,
        *,
        cron_expression: builtins.str,
        name: builtins.str,
        job_names: typing.Optional[typing.List[builtins.str]] = None,
        tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]] = None,
    ) -> None:
        """Properties for defining a ``AWS::DataBrew::Schedule``.

        :param cron_expression: ``AWS::DataBrew::Schedule.CronExpression``.
        :param name: ``AWS::DataBrew::Schedule.Name``.
        :param job_names: ``AWS::DataBrew::Schedule.JobNames``.
        :param tags: ``AWS::DataBrew::Schedule.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-schedule.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "cron_expression": cron_expression,
            "name": name,
        }
        if job_names is not None:
            self._values["job_names"] = job_names
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def cron_expression(self) -> builtins.str:
        """``AWS::DataBrew::Schedule.CronExpression``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-schedule.html#cfn-databrew-schedule-cronexpression
        """
        result = self._values.get("cron_expression")
        assert result is not None, "Required property 'cron_expression' is missing"
        return result

    @builtins.property
    def name(self) -> builtins.str:
        """``AWS::DataBrew::Schedule.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-schedule.html#cfn-databrew-schedule-name
        """
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return result

    @builtins.property
    def job_names(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::DataBrew::Schedule.JobNames``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-schedule.html#cfn-databrew-schedule-jobnames
        """
        result = self._values.get("job_names")
        return result

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        """``AWS::DataBrew::Schedule.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-schedule.html#cfn-databrew-schedule-tags
        """
        result = self._values.get("tags")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnScheduleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnDataset",
    "CfnDatasetProps",
    "CfnJob",
    "CfnJobProps",
    "CfnProject",
    "CfnProjectProps",
    "CfnRecipe",
    "CfnRecipeProps",
    "CfnSchedule",
    "CfnScheduleProps",
]

publication.publish()
