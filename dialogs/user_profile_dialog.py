# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.dialogs import (
    ComponentDialog,
    WaterfallDialog,
    WaterfallStepContext,
    DialogTurnResult,
)
from botbuilder.dialogs.prompts import (
    TextPrompt,
    NumberPrompt,
    ChoicePrompt,
    ConfirmPrompt,
    AttachmentPrompt,
    PromptOptions,
    PromptValidatorContext,
)
from botbuilder.dialogs.choices import Choice
from botbuilder.core import MessageFactory, UserState

from data_models import UserProfile

import smtplib



class UserProfileDialog(ComponentDialog):
    def __init__(self, user_state: UserState):
        super(UserProfileDialog, self).__init__(UserProfileDialog.__name__)

        self.user_profile_accessor = user_state.create_property("UserProfile")

        self.add_dialog(
            WaterfallDialog(
                WaterfallDialog.__name__,
                [
                    self.first_step,
                    self.second_step,
                    self.third_step,
                    self.fourth_step,
                    self.fifth_step,
                    self.sixth_step,
                    self.seventh_step,
                    self.eighth_step,
                    
                ],
            )
        )
        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(
            NumberPrompt(NumberPrompt.__name__, UserProfileDialog.age_prompt_validator)
        )
        self.add_dialog(ChoicePrompt(ChoicePrompt.__name__))
        self.add_dialog(ConfirmPrompt(ConfirmPrompt.__name__))
        self.add_dialog(
            AttachmentPrompt(
                AttachmentPrompt.__name__, UserProfileDialog.picture_prompt_validator
            )
        )

        self.initial_dialog_id = WaterfallDialog.__name__

    async def first_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        # WaterfallStep always finishes with the end of the Waterfall or with another dialog;
        # here it is a Prompt Dialog. Running a prompt here means the next WaterfallStep will
        await step_context.context.send_activity(
                MessageFactory.text(f"Hey Welcome!")
            )
        # be run when the users response is received.
        return await step_context.prompt(
            ConfirmPrompt.__name__,
            PromptOptions(
                prompt=MessageFactory.text("Are you a new employee?"),
                
            ),
        )

    async def second_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        if step_context.result:
            # step_context.values["transport"] = step_context.result.value
            # employee=step_context.result.value
            step_context.values['employee_id']='Required'
            return await step_context.prompt(
                ConfirmPrompt.__name__,
                PromptOptions(prompt=MessageFactory.text("Do you have an employee Id?.")),
            )
        else:
            step_context.values["employee_id"]='Approved'
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(prompt=MessageFactory.text("What is your employee id?.")),
                )

    async def third_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        step_context.values["get_employee_id"]=False
        if step_context.values['employee_id'] == 'Required':

            if step_context.result != True:

            #step_context.values["name"] = step_context.result

            # We can send messages to the user at any point in the WaterfallStep.
                await step_context.context.send_activity(
                    MessageFactory.text(f"You need to get your employee Id created first")
                )
                
                step_context.values["get_employee_id"]=True
                get_employee_id=step_context.values["get_employee_id"]
                # WaterfallStep always finishes with the end of the Waterfall or
                # with another dialog; here it is a Prompt Dialog.
                return await step_context.prompt(
                    ConfirmPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text("Would you like me to put in a request to HR to get your employee Id created")

                        ),
                )
            else:
                step_context.values["get_employee_id"]=False
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text("Please Provide Your Employee ID.")
                       ),

          
               )
        return await step_context.next(1)
    
    async def fourth_step(self,step_context: WaterfallStepContext) -> DialogTurnResult:
       
        if step_context.values["get_employee_id"]==True:
            if step_context.result:
                await step_context.context.send_activity(
                        MessageFactory.text(f" We have informed to our HR team.They will revert you back")

                )

                gmail_user = 'botframe007@gmail.com'
                gmail_password = 'Yogesh@123'

                sent_from = gmail_user
                to = ['abhi05jan@gmail.com']
                subject = 'MSG Subject'
                body = 'Hey,Hows you'

                email_text = """\
                From: %s
                To: %s
                Subject: %s

                %s
                """ % (sent_from, ", ".join(to), subject, body)

                try:
                    
                    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                    server.ehlo()
                    server.login(gmail_user, gmail_password)
                    server.sendmail(sent_from, to, email_text)
                    server.close()

                    print ('Email sent!')
                except:
                    print ('Something went wrong...')

                return await step_context.end_dialog()

            else:

                await step_context.context.send_activity(
                        MessageFactory.text(f"Is there anything else i can help you with? ")
                )

                return await step_context.end_dialog()
        employee_id=step_context.result

        await step_context.context.send_activity(
            MessageFactory.text(f"Thank You ")
        )
        return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text("What application/folder do you need access to ?.")
                ),
        )
        


    async def fifth_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        step_context.values['access']=step_context.result
        await step_context.context.send_activity(
            MessageFactory.text(f"Thank You ")
        )


        await step_context.context.send_activity(
            MessageFactory.text(f"I need your manager’s approval before granting access.")
        )
        return await step_context.prompt(
            ConfirmPrompt.__name__,
            PromptOptions(
                prompt=MessageFactory.text("Is Saurabh Your Reporting Manager?"),
                
            ),
        )


    async def sixth_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        folder_access=step_context.values['access']

        if step_context.result:
            step_context.values['reporting_manager']=False
            step_context.values['folder_name']=folder_access
            return await step_context.prompt(

                ConfirmPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text(f"Is it Ok if I send an email to Saurabh requesting permission for you to access {folder_access}?"),
                    
                ),
        )
        else:
            step_context.values['reporting_manager']=True
            
            step_context.values['folder_name']=folder_access
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text(f"Please provide your reporting manager name"),
                    
                ),
        )

    async def seventh_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        folder_access=step_context.values['folder_name']
        if step_context.values['reporting_manager']==True:
            manager_name=step_context.result
            return await step_context.prompt(
                ConfirmPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text(f"Is it Ok if I send an email to {manager_name} requesting permission for you to access {folder_access}?"),
                    
                ),
        )
        else:
           await step_context.context.send_activity(
            MessageFactory.text(f"Thanks, someone from the Helpdesk will be with you shortly!")
            )
           return await step_context.end_dialog()

    async def eighth_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        if step_context.result:
            await step_context.context.send_activity(
            MessageFactory.text(f"Thanks, someone from the Helpdesk will be with you shortly!")
            )
            return await step_context.end_dialog()
               
        



    async def picture_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        age = step_context.result
        step_context.values["age"] = age

        msg = (
            "No age given."
            if step_context.result == -1
            else f"I have your age as {age}."
        )

        # We can send messages to the user at any point in the WaterfallStep.
        await step_context.context.send_activity(MessageFactory.text(msg))

        if step_context.context.activity.channel_id == "msteams":
            # This attachment prompt example is not designed to work for Teams attachments, so skip it in this case
            await step_context.context.send_activity(
                "Skipping attachment prompt in Teams channel..."
            )
            return await step_context.next(None)

        # WaterfallStep always finishes with the end of the Waterfall or with another dialog; here it is a Prompt
        # Dialog.
        prompt_options = PromptOptions(
            prompt=MessageFactory.text(
                "Please attach a profile picture (or type any message to skip)."
            ),
            retry_prompt=MessageFactory.text(
                "The attachment must be a jpeg/png image file."
            ),
        )
        return await step_context.prompt(AttachmentPrompt.__name__, prompt_options)

    async def confirm_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        step_context.values["picture"] = (
            None if not step_context.result else step_context.result[0]
        )

        # WaterfallStep always finishes with the end of the Waterfall or
        # with another dialog; here it is a Prompt Dialog.
        return await step_context.prompt(
            ConfirmPrompt.__name__,
            PromptOptions(prompt=MessageFactory.text("Is this ok?")),
        )

    async def summary_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        if step_context.result:
            # Get the current profile object from user state.  Changes to it
            # will saved during Bot.on_turn.
            user_profile = await self.user_profile_accessor.get(
                step_context.context, UserProfile
            )

            user_profile.transport = step_context.values["transport"]
            user_profile.name = step_context.values["name"]
            user_profile.age = step_context.values["age"]
            user_profile.picture = step_context.values["picture"]

            msg = f"I have your mode of transport as {user_profile.transport} and your name as {user_profile.name}."
            if user_profile.age != -1:
                msg += f" And age as {user_profile.age}."

            await step_context.context.send_activity(MessageFactory.text(msg))

            if user_profile.picture:
                await step_context.context.send_activity(
                    MessageFactory.attachment(
                        user_profile.picture, "This is your profile picture."
                    )
                )
            else:
                await step_context.context.send_activity(
                    "A profile picture was saved but could not be displayed here."
                )
        else:
            await step_context.context.send_activity(
                MessageFactory.text("Thanks. Your profile will not be kept.")
            )

        # WaterfallStep always finishes with the end of the Waterfall or with another
        # dialog, here it is the end.
        return await step_context.end_dialog()

    @staticmethod
    async def age_prompt_validator(prompt_context: PromptValidatorContext) -> bool:
        # This condition is our validation rule. You can also change the value at this point.
        return (
            prompt_context.recognized.succeeded
            and 0 < prompt_context.recognized.value < 150
        )

    @staticmethod
    async def picture_prompt_validator(prompt_context: PromptValidatorContext) -> bool:
        if not prompt_context.recognized.succeeded:
            await prompt_context.context.send_activity(
                "No attachments received. Proceeding without a profile picture..."
            )

            # We can return true from a validator function even if recognized.succeeded is false.
            return True

        attachments = prompt_context.recognized.value

        valid_images = [
            attachment
            for attachment in attachments
            if attachment.content_type in ["image/jpeg", "image/png"]
        ]

        prompt_context.recognized.value = valid_images

        # If none of the attachments are valid images, the retry prompt should be sent.
        return len(valid_images) > 0
